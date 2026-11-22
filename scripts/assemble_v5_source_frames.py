from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

import av
import numpy as np
from PIL import Image


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def decode_rgb(path: Path) -> list[np.ndarray]:
    container = av.open(str(path))
    frames: list[np.ndarray] = []
    try:
        for frame in container.decode(video=0):
            frames.append(frame.to_ndarray(format="rgb24"))
    finally:
        container.close()
    if not frames:
        raise RuntimeError(f"No video frames decoded from {path}")
    return frames


def save_frame(array: np.ndarray, path: Path) -> None:
    Image.fromarray(array, mode="RGB").save(path, format="PNG", optimize=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble the mixed-resolution v5 source sequence.")
    parser.add_argument("--scene01", type=Path)
    parser.add_argument(
        "--scene01-frame-dir",
        type=Path,
        help="Optional directory containing exactly frame_001.png..frame_048.png; preferred for the FILM-cleaned scene 01.",
    )
    parser.add_argument("--scene04", type=Path, required=True)
    parser.add_argument(
        "--base-frame-dir",
        type=Path,
        default=PACKAGE_ROOT / "outputs" / "upscaled_frames",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PACKAGE_ROOT / "outputs" / "source_frames_v5",
    )
    parser.add_argument("--scene01-start", type=int, default=0)
    parser.add_argument("--scene04-start", type=int, default=0)
    parser.add_argument("--count", type=int, default=48)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.scene01 is None and args.scene01_frame_dir is None:
        raise ValueError("Provide either --scene01 or --scene01-frame-dir")
    if args.scene01 is not None and not args.scene01.is_file():
        raise FileNotFoundError(args.scene01)
    if not args.scene04.is_file():
        raise FileNotFoundError(args.scene04)
    base_frames = sorted(args.base_frame_dir.glob("source_*.png"))
    if len(base_frames) != 240:
        raise RuntimeError(f"Expected 240 approved base frames, found {len(base_frames)}")

    if args.scene01_frame_dir is not None:
        scene01_paths = sorted(args.scene01_frame_dir.glob("frame_*.png"))
        if len(scene01_paths) != args.count:
            raise RuntimeError(
                f"Expected {args.count} scene01 PNG frames, found {len(scene01_paths)}"
            )
        scene01 = [np.asarray(Image.open(path).convert("RGB")) for path in scene01_paths]
        selected01 = scene01
    else:
        scene01 = decode_rgb(args.scene01)
        selected01 = scene01[args.scene01_start : args.scene01_start + args.count]
    scene04 = decode_rgb(args.scene04)
    selected04 = scene04[args.scene04_start : args.scene04_start + args.count]
    if len(selected01) != args.count or len(selected04) != args.count:
        raise RuntimeError(
            f"Selection too short: scene01={len(selected01)}, scene04={len(selected04)}, expected={args.count}"
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    for stale in args.output_dir.glob("source_*.png"):
        stale.unlink()

    for offset, frame in enumerate(selected01, start=1):
        save_frame(frame, args.output_dir / f"source_{offset:05d}.png")
    for one_based in range(49, 145):
        shutil.copy2(
            args.base_frame_dir / f"source_{one_based:05d}.png",
            args.output_dir / f"source_{one_based:05d}.png",
        )
    for offset, frame in enumerate(selected04, start=145):
        save_frame(frame, args.output_dir / f"source_{offset:05d}.png")
    for one_based in range(193, 241):
        shutil.copy2(
            args.base_frame_dir / f"source_{one_based:05d}.png",
            args.output_dir / f"source_{one_based:05d}.png",
        )

    written = sorted(args.output_dir.glob("source_*.png"))
    if len(written) != 240:
        raise AssertionError(len(written))
    manifest = {
        "project": "PhotoDay H3 v5 selective scene repair",
        "scene01_source": str(args.scene01_frame_dir or args.scene01),
        "scene01_source_type": "lossless PNG sequence" if args.scene01_frame_dir else "video",
        "scene01_sha256": sha256(args.scene01) if args.scene01 else None,
        "scene01_selection_zero_based": None if args.scene01_frame_dir else [args.scene01_start, args.scene01_start + args.count - 1],
        "scene04_source": str(args.scene04),
        "scene04_sha256": sha256(args.scene04),
        "scene04_selection_zero_based": [args.scene04_start, args.scene04_start + args.count - 1],
        "locked_base_ranges_one_based": ["49-144", "193-240"],
        "output_pattern": str(args.output_dir / "source_%05d.png"),
        "frame_count": 240,
        "fps": 24,
    }
    manifest_path = PACKAGE_ROOT / "workflow" / "source_assembly_manifest_v5.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote 240 v5 source frames to {args.output_dir}", flush=True)
    print(f"wrote {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
