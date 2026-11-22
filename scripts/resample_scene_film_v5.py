from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import av
import numpy as np
import torch
from PIL import Image


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMFY_ROOT = Path(r"C:\Users\Vadim\ComfyUI")
DEFAULT_MODEL = (
    DEFAULT_COMFY_ROOT
    / "models"
    / "frame_interpolation"
    / "film_net_fp16.safetensors"
)


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
        raise RuntimeError(f"No frames decoded from {path}")
    return frames


def load_film(comfy_root: Path, model_path: Path, device: torch.device):
    if str(comfy_root) not in sys.path:
        sys.path.insert(0, str(comfy_root))
    import comfy.utils
    from comfy_extras.frame_interpolation_models.film_net import FILMNet

    state = comfy.utils.load_torch_file(str(model_path), safe_load=True)
    model = FILMNet()
    model.load_state_dict(state)
    dtype = torch.float16 if device.type == "cuda" else torch.float32
    model.eval().to(device=device, dtype=dtype)
    print(f"loaded FILM on {device} as {dtype}", flush=True)
    return model, dtype


def to_tensor(frame: np.ndarray, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
    tensor = torch.from_numpy(frame.astype(np.float32) / 255.0)
    return tensor.permute(2, 0, 1).unsqueeze(0).to(device=device, dtype=dtype)


@torch.inference_mode()
def interpolate(
    first: np.ndarray,
    second: np.ndarray,
    fraction: float,
    model,
    device: torch.device,
    dtype: torch.dtype,
) -> np.ndarray:
    if fraction <= 1e-8:
        return first
    if fraction >= 1.0 - 1e-8:
        return second
    image0 = to_tensor(first, device, dtype)
    image1 = to_tensor(second, device, dtype)
    result = model(image0, image1, timestep=float(fraction))
    result = result[0].permute(1, 2, 0).float().clamp(0.0, 1.0).cpu()
    return (result.numpy() * 255.0 + 0.5).astype(np.uint8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Resample an approved clean H3 frame window to an exact delivery length with FILM."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-start", type=int, default=0, help="Zero-based source frame.")
    parser.add_argument("--source-count", type=int, required=True)
    parser.add_argument("--output-count", type=int, default=48)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--device", default="cuda")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for required in (args.input, args.model):
        if not required.is_file():
            raise FileNotFoundError(required)
    if args.source_count < 2 or args.output_count < 2:
        raise ValueError("source-count and output-count must both be at least 2")
    decoded = decode_rgb(args.input)
    source = decoded[args.source_start : args.source_start + args.source_count]
    if len(source) != args.source_count:
        raise RuntimeError(f"Requested {args.source_count} source frames, found {len(source)}")

    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    model, dtype = load_film(args.comfy_root, args.model, device)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    for stale in args.output_dir.glob("frame_*.png"):
        stale.unlink()

    positions: list[float] = []
    for output_index in range(args.output_count):
        position = output_index * (args.source_count - 1) / (args.output_count - 1)
        left = min(math.floor(position), args.source_count - 1)
        right = min(left + 1, args.source_count - 1)
        fraction = position - left
        frame = interpolate(source[left], source[right], fraction, model, device, dtype)
        path = args.output_dir / f"frame_{output_index + 1:03d}.png"
        Image.fromarray(frame, mode="RGB").save(path, format="PNG", optimize=False)
        positions.append(position + args.source_start)
        print(
            f"[{output_index + 1:02d}/{args.output_count}] source={position + args.source_start:.4f}",
            flush=True,
        )

    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    manifest = {
        "project": "PhotoDay H3 v5 selective scene repair",
        "method": "FILM arbitrary-timestep temporal resampling",
        "input": str(args.input),
        "input_sha256": sha256(args.input),
        "source_window_zero_based": [
            args.source_start,
            args.source_start + args.source_count - 1,
        ],
        "rejected_reason_after_window": "H3 began turning candle flames into starburst rays; rejected frames are not used.",
        "output_count": args.output_count,
        "output_pattern": str(args.output_dir / "frame_%03d.png"),
        "source_positions": positions,
        "model": str(args.model),
        "model_sha256": sha256(args.model),
    }
    manifest_path = args.output_dir / "resample_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {args.output_count} frames and {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
