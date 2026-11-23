#!/usr/bin/env python3
"""Validate an H3 scene contract without third-party dependencies."""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any


MODES = {"t2va", "i2va", "fl2va", "ref2va", "multiframe_control"}
REFERENCE_KINDS = {"image", "video", "audio"}
HANDS = {"left", "right", "both", "none"}
POST_INTERPOLATION_POLICIES = {
    "forbidden",
    "optional_after_native_pass",
    "required_after_native_pass",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract", type=Path, help="Path to scene-contract JSON")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the validation result as JSON.",
    )
    return parser.parse_args()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def validate(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["root must be a JSON object"], warnings

    required = (
        "scene_id",
        "intent",
        "duration_seconds",
        "fps",
        "aspect_ratio",
        "mode",
        "inputs",
        "subjects",
        "timeline",
        "camera",
        "acceptance",
    )
    for key in required:
        if key not in data:
            errors.append(f"missing required field: {key}")

    duration = data.get("duration_seconds")
    if not is_number(duration):
        errors.append("duration_seconds must be a number")
        duration_value = None
    else:
        duration_value = float(duration)
        if not 4.0 <= duration_value <= 15.0:
            errors.append("duration_seconds must be within H3's 4–15 second range")

    fps = data.get("fps")
    if fps != 24:
        errors.append("fps must be 24 for H3 generation")

    mode = data.get("mode")
    if mode not in MODES:
        errors.append(f"mode must be one of: {', '.join(sorted(MODES))}")

    inputs = data.get("inputs")
    if not isinstance(inputs, dict):
        errors.append("inputs must be an object")
        anchors: list[Any] = []
        references: list[Any] = []
    else:
        anchors = inputs.get("frame_anchors", [])
        references = inputs.get("references", [])
        if not isinstance(anchors, list):
            errors.append("inputs.frame_anchors must be an array")
            anchors = []
        if not isinstance(references, list):
            errors.append("inputs.references must be an array")
            references = []

    expected_anchor_counts = {"t2va": 0, "i2va": 1, "fl2va": 2, "ref2va": 0}
    if mode in expected_anchor_counts and len(anchors) != expected_anchor_counts[mode]:
        errors.append(
            f"{mode} requires {expected_anchor_counts[mode]} frame anchor(s), "
            f"found {len(anchors)}"
        )
    if mode != "ref2va" and references:
        errors.append("reference media require ref2va; do not mix conditioning families")
    if mode == "ref2va" and not references:
        errors.append("ref2va requires at least one labelled reference")
    if mode == "multiframe_control" and not anchors:
        warnings.append("multiframe_control normally needs at least one structural anchor")

    reference_counts = {kind: 0 for kind in REFERENCE_KINDS}
    reference_labels: set[str] = set()
    for index, reference in enumerate(references):
        if not isinstance(reference, dict):
            errors.append(f"reference {index} must be an object")
            continue
        kind = reference.get("kind")
        label = reference.get("label")
        if kind not in REFERENCE_KINDS:
            errors.append(f"reference {index} kind must be image, video, or audio")
        else:
            reference_counts[kind] += 1
        if not isinstance(label, str) or not label.strip():
            errors.append(f"reference {index} needs a non-empty label")
        elif label in reference_labels:
            errors.append(f"duplicate reference label: {label}")
        else:
            reference_labels.add(label)
    if reference_counts["image"] > 9:
        errors.append("ref2va supports at most 9 image references")
    if reference_counts["video"] > 3:
        errors.append("ref2va supports at most 3 video references")
    if reference_counts["audio"] > 3:
        errors.append("ref2va supports at most 3 audio references")
    if len(references) > 12:
        errors.append("ref2va supports at most 12 references total")

    subjects = data.get("subjects")
    subject_ids: set[str] = set()
    if not isinstance(subjects, list) or not subjects:
        errors.append("subjects must be a non-empty array")
        subjects = []
    for index, subject in enumerate(subjects):
        if not isinstance(subject, dict):
            errors.append(f"subject {index} must be an object")
            continue
        subject_id = subject.get("id")
        if not isinstance(subject_id, str) or not subject_id.strip():
            errors.append(f"subject {index} needs a non-empty id")
        elif subject_id in subject_ids:
            errors.append(f"duplicate subject id: {subject_id}")
        else:
            subject_ids.add(subject_id)
        count = subject.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            errors.append(f"subject {subject_id or index} count must be a positive integer")
        visible_hands = subject.get("visible_hands")
        if (
            not isinstance(visible_hands, int)
            or isinstance(visible_hands, bool)
            or not 0 <= visible_hands <= 2
        ):
            errors.append(
                f"subject {subject_id or index} visible_hands must be an integer from 0 to 2"
            )

    props = data.get("props", [])
    prop_ids: set[str] = set()
    if not isinstance(props, list):
        errors.append("props must be an array")
        props = []
    for index, prop in enumerate(props):
        if not isinstance(prop, dict):
            errors.append(f"prop {index} must be an object")
            continue
        prop_id = prop.get("id")
        if not isinstance(prop_id, str) or not prop_id.strip():
            errors.append(f"prop {index} needs a non-empty id")
        elif prop_id in prop_ids:
            errors.append(f"duplicate prop id: {prop_id}")
        else:
            prop_ids.add(prop_id)
        owner = prop.get("owner")
        if owner not in subject_ids and owner != "environment":
            errors.append(f"prop {prop_id or index} has unknown owner: {owner!r}")
        if prop.get("hand") not in HANDS:
            errors.append(
                f"prop {prop_id or index} hand must be one of: {', '.join(sorted(HANDS))}"
            )
        count = prop.get("count")
        if not isinstance(count, int) or isinstance(count, bool) or count < 1:
            errors.append(f"prop {prop_id or index} count must be a positive integer")

    timeline = data.get("timeline")
    if not isinstance(timeline, list) or not timeline:
        errors.append("timeline must be a non-empty array")
        timeline = []
    cursor = 0.0
    for index, beat in enumerate(timeline):
        if not isinstance(beat, dict):
            errors.append(f"timeline item {index} must be an object")
            continue
        start = beat.get("start")
        end = beat.get("end")
        if not is_number(start) or not is_number(end):
            errors.append(f"timeline item {index} start/end must be numbers")
            continue
        start_value = float(start)
        end_value = float(end)
        if not math.isclose(start_value, cursor, abs_tol=0.001):
            errors.append(
                f"timeline item {index} starts at {start_value}, expected {cursor}"
            )
        if end_value <= start_value:
            errors.append(f"timeline item {index} end must be after start")
        cursor = end_value
        if not str(beat.get("state_change", "")).strip():
            errors.append(f"timeline item {index} needs a visible state_change")
    if duration_value is not None and timeline:
        if not math.isclose(cursor, duration_value, abs_tol=0.001):
            errors.append(
                f"timeline ends at {cursor}, expected duration {duration_value}"
            )

    motion = data.get("motion")
    if motion is None:
        warnings.append(
            "no motion envelope is defined; add path, cadence, easing, allowed body "
            "motion, locked contacts, direction changes, and interpolation policy"
        )
    elif not isinstance(motion, dict):
        errors.append("motion must be an object")
    else:
        for key in (
            "path",
            "cadence",
            "easing",
            "allowed_body_motion",
            "locked_contacts",
        ):
            if not isinstance(motion.get(key), str) or not motion[key].strip():
                errors.append(f"motion.{key} must be a non-empty string")
        direction_changes = motion.get("direction_changes")
        if (
            not isinstance(direction_changes, int)
            or isinstance(direction_changes, bool)
            or direction_changes < 0
        ):
            errors.append("motion.direction_changes must be a non-negative integer")
        policy = motion.get("post_interpolation")
        if policy not in POST_INTERPOLATION_POLICIES:
            errors.append(
                "motion.post_interpolation must be one of: "
                + ", ".join(sorted(POST_INTERPOLATION_POLICIES))
            )
        for index, beat in enumerate(timeline):
            if isinstance(beat, dict) and not str(
                beat.get("motion_continuity", "")
            ).strip():
                warnings.append(
                    f"timeline item {index} has no motion_continuity clause"
                )

    acceptance = data.get("acceptance")
    if not isinstance(acceptance, list) or not acceptance:
        errors.append("acceptance must be a non-empty array")
    elif any(not isinstance(item, str) or not item.strip() for item in acceptance):
        errors.append("every acceptance item must be a non-empty string")

    if not data.get("locks"):
        warnings.append("no continuity locks are defined")
    if not props:
        warnings.append("no props are declared; confirm the shot truly has none")

    return errors, warnings


def main() -> int:
    args = parse_args()
    try:
        data = json.loads(args.contract.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: file not found: {args.contract}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate(data)
    result = {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "contract": str(args.contract),
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = "PASS" if not errors else "FAIL"
        print(f"{status}: {args.contract}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
