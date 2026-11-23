#!/usr/bin/env python3
"""Report normalized adjacent-frame motion deltas with ffmpeg.

The report is diagnostic evidence, not an automated quality verdict. Large deltas
can be intentional cuts; small deltas can be intentional holds.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import subprocess
from pathlib import Path


FRAME_RE = re.compile(r"frame:(\d+)")
PTS_RE = re.compile(r"pts_time:([0-9.]+)")
YAVG_RE = re.compile(r"lavfi\.signalstats\.YAVG=([0-9.]+)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--roi",
        help="Optional crop x:y:w:h before normalized analysis, for example 120:40:300:260.",
    )
    parser.add_argument("--width", type=int, default=256)
    return parser.parse_args()


def percentile(values: list[float], fraction: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * fraction
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def probe(path: Path) -> dict:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=width,height,avg_frame_rate,nb_frames,duration",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def motion_rows(path: Path, width: int, roi: str | None) -> list[dict]:
    filters = []
    if roi:
        parts = roi.split(":")
        if len(parts) != 4 or any(not part.isdigit() for part in parts):
            raise ValueError("--roi must be x:y:w:h using non-negative integers")
        x, y, w, h = parts
        filters.append(f"crop={w}:{h}:{x}:{y}")
    filters.extend(
        [
            f"scale={width}:-2:flags=area",
            "format=gray",
            "tblend=all_mode=difference",
            "signalstats",
            "metadata=print",
        ]
    )
    result = subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "info",
            "-i",
            str(path),
            "-vf",
            ",".join(filters),
            "-f",
            "null",
            "-",
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    rows: list[dict] = []
    current_frame: int | None = None
    current_time: float | None = None
    for line in result.stderr.splitlines():
        frame_match = FRAME_RE.search(line)
        if frame_match:
            current_frame = int(frame_match.group(1))
            pts_match = PTS_RE.search(line)
            current_time = float(pts_match.group(1)) if pts_match else None
            continue
        yavg_match = YAVG_RE.search(line)
        if yavg_match and current_frame is not None:
            rows.append(
                {
                    "frame": current_frame,
                    "time_seconds": current_time,
                    "mean_abs_luma_delta": float(yavg_match.group(1)),
                }
            )
    if not rows:
        raise RuntimeError("ffmpeg returned no signalstats motion rows")
    return rows


def summarize(rows: list[dict]) -> dict:
    values = [row["mean_abs_luma_delta"] for row in rows]
    median = statistics.median(values)
    deviations = [abs(value - median) for value in values]
    mad = statistics.median(deviations)
    spike_threshold = median + max(4.0 * mad, 0.5)
    freeze_threshold = max(0.05, median * 0.25)
    spikes = [row for row in rows if row["mean_abs_luma_delta"] > spike_threshold]
    freezes = [row for row in rows if row["mean_abs_luma_delta"] < freeze_threshold]
    return {
        "sample_count": len(values),
        "mean": statistics.fmean(values),
        "median": median,
        "p05": percentile(values, 0.05),
        "p95": percentile(values, 0.95),
        "max": max(values),
        "median_absolute_deviation": mad,
        "diagnostic_thresholds": {
            "spike_above": spike_threshold,
            "freeze_below": freeze_threshold,
        },
        "spike_count": len(spikes),
        "freeze_count": len(freezes),
        "largest_deltas": sorted(
            rows, key=lambda row: row["mean_abs_luma_delta"], reverse=True
        )[:12],
        "spike_frames": [row["frame"] for row in spikes],
        "freeze_frames": [row["frame"] for row in freezes],
    }


def main() -> int:
    args = parse_args()
    if not args.video.is_file():
        raise SystemExit(f"video not found: {args.video}")
    report = {
        "video": str(args.video.resolve()),
        "roi": args.roi,
        "normalized_width": args.width,
        "probe": probe(args.video),
    }
    rows = motion_rows(args.video, args.width, args.roi)
    report["summary"] = summarize(rows)
    report["frames"] = rows
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
