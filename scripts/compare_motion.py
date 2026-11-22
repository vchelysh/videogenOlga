from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import av
import numpy as np


def frame_motion(path: Path) -> list[dict]:
    rows: list[dict] = []
    previous = None
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        for index, frame in enumerate(container.decode(stream)):
            gray = frame.to_ndarray(format="gray")[::4, ::4].astype(np.int16)
            if previous is None:
                mad = 0.0
                changed = 0.0
            else:
                delta = np.abs(gray - previous)
                mad = float(delta.mean())
                changed = float((delta >= 4).mean() * 100.0)
            rows.append(
                {
                    "frame": index,
                    "time": index / float(stream.average_rate),
                    "mean_abs_luma_delta": mad,
                    "changed_pixels_pct": changed,
                }
            )
            previous = gray
    return rows


def summarize(rows: list[dict], scene_frames: int = 48) -> list[dict]:
    summaries = []
    for scene in range(5):
        start = scene * scene_frames
        end = min((scene + 1) * scene_frames, len(rows))
        values = np.array(
            [row["mean_abs_luma_delta"] for row in rows[start + 1 : end]], dtype=np.float64
        )
        changed = np.array(
            [row["changed_pixels_pct"] for row in rows[start + 1 : end]], dtype=np.float64
        )
        summaries.append(
            {
                "scene": scene + 1,
                "frames": f"{start}-{end - 1}",
                "motion_mean": float(values.mean()) if values.size else 0.0,
                "motion_median": float(np.median(values)) if values.size else 0.0,
                "motion_p95": float(np.percentile(values, 95)) if values.size else 0.0,
                "changed_pixels_mean_pct": float(changed.mean()) if changed.size else 0.0,
            }
        )
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser(description="Frame-by-frame temporal-motion comparison.")
    parser.add_argument("--video", action="append", required=True, type=Path)
    parser.add_argument("--label", action="append", required=True)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    if len(args.video) != len(args.label):
        raise SystemExit("Each --video needs one --label")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    report = {}
    for label, path in zip(args.label, args.video):
        rows = frame_motion(path)
        with (args.output_dir / f"motion_{label}.csv").open("w", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
        report[label] = {
            "path": str(path.resolve()),
            "frame_count": len(rows),
            "scenes": summarize(rows),
        }

    labels = list(report)
    if "v1" in report:
        baseline = report["v1"]["scenes"]
        for label in labels:
            for base_scene, scene in zip(baseline, report[label]["scenes"]):
                denom = base_scene["motion_mean"] or 1.0
                scene["motion_vs_v1_ratio"] = scene["motion_mean"] / denom

    (args.output_dir / "motion_summary.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
