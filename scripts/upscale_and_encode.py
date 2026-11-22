from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageFilter
from spandrel import ImageModelDescriptor, ModelLoader


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMFY_ROOT = Path(r"C:\Users\Vadim\ComfyUI")
DEFAULT_MODEL = DEFAULT_COMFY_ROOT / "models" / "upscale_models" / "RealESRGAN_x4plus.pth"
DEFAULT_AUDIO = PACKAGE_ROOT / "references" / "PhotoDay_v1_motion_master.mp4"


def run(command: list[str]) -> None:
    print(" ".join(command), flush=True)
    subprocess.run(command, check=True)


def cover_crop(image: Image.Image, width: int, height: int) -> Image.Image:
    source_ratio = image.width / image.height
    target_ratio = width / height
    if source_ratio > target_ratio:
        resized_height = height
        resized_width = round(image.width * height / image.height)
    else:
        resized_width = width
        resized_height = round(image.height * width / image.width)
    resized = image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
    left = max(0, (resized.width - width) // 2)
    top = max(0, (resized.height - height) // 2)
    return resized.crop((left, top, left + width, top + height))


def load_upscaler(model_path: Path, device: torch.device) -> ImageModelDescriptor:
    descriptor = ModelLoader().load_from_file(model_path).eval()
    if not isinstance(descriptor, ImageModelDescriptor):
        raise TypeError(f"Not a single-image upscaler: {type(descriptor)!r}")
    descriptor = descriptor.to(device)
    print(
        f"loaded {model_path.name}: scale={descriptor.scale}, device={device}",
        flush=True,
    )
    return descriptor


@torch.inference_mode()
def upscale_frame(
    source: Image.Image,
    model: ImageModelDescriptor,
    device: torch.device,
    tile: int,
    overlap: int,
    comfy_root: Path,
) -> Image.Image:
    if str(comfy_root) not in sys.path:
        sys.path.insert(0, str(comfy_root))
    import comfy.utils

    rgb = np.asarray(source.convert("RGB"), dtype=np.float32) / 255.0
    tensor = torch.from_numpy(rgb).permute(2, 0, 1).unsqueeze(0).to(device)
    result = comfy.utils.tiled_scale(
        tensor,
        lambda tile_tensor: model(tile_tensor.float()),
        tile_x=tile,
        tile_y=tile,
        overlap=overlap,
        upscale_amount=float(model.scale),
        output_device=torch.device("cpu"),
    )
    result = result.squeeze(0).permute(1, 2, 0).clamp(0.0, 1.0)
    array = (result.numpy() * 255.0 + 0.5).astype(np.uint8)
    return Image.fromarray(array, mode="RGB")


def extract_frames(input_video: Path, frame_dir: Path, frame_count: int) -> None:
    frame_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(frame_dir.glob("source_*.png"))
    if len(existing) == frame_count:
        print(f"reusing {len(existing)} extracted frames", flush=True)
        return
    for path in existing:
        path.unlink()
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-i",
            str(input_video),
            "-vf",
            "fps=24",
            "-frames:v",
            str(frame_count),
            str(frame_dir / "source_%05d.png"),
        ]
    )


def process_frames(
    source_frame_dir: Path,
    output_frame_dir: Path,
    model: ImageModelDescriptor,
    device: torch.device,
    comfy_root: Path,
    frame_count: int,
    width: int,
    height: int,
    tile: int,
    overlap: int,
    sr_blend: float,
    unsharp_radius: float,
    unsharp_percent: int,
    unsharp_threshold: int,
) -> None:
    output_frame_dir.mkdir(parents=True, exist_ok=True)
    for index in range(1, frame_count + 1):
        source_path = source_frame_dir / f"source_{index:05d}.png"
        output_path = output_frame_dir / f"upscaled_{index:05d}.png"
        if output_path.is_file():
            print(f"[{index:03d}/{frame_count}] reuse {output_path.name}", flush=True)
            continue
        with Image.open(source_path) as loaded:
            source = loaded.convert("RGB")
        lanczos = cover_crop(source, width, height)
        sr_full = upscale_frame(source, model, device, tile, overlap, comfy_root)
        sr_target = cover_crop(sr_full, width, height)
        final = Image.blend(lanczos, sr_target, sr_blend)
        if unsharp_percent > 0:
            final = final.filter(
                ImageFilter.UnsharpMask(
                    radius=unsharp_radius,
                    percent=unsharp_percent,
                    threshold=unsharp_threshold,
                )
            )
        final.save(output_path, format="PNG", optimize=False)
        print(f"[{index:03d}/{frame_count}] wrote {output_path.name}", flush=True)


def encode(
    frame_dir: Path,
    audio_from: Path,
    output_video: Path,
    fps: int,
    frame_count: int,
    crf: int,
    preset: str,
    tune: str | None,
) -> None:
    output_video.parent.mkdir(parents=True, exist_ok=True)
    duration = frame_count / fps
    run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-framerate",
            str(fps),
            "-i",
            str(frame_dir / "upscaled_%05d.png"),
            "-i",
            str(audio_from),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0?",
            "-frames:v",
            str(frame_count),
            "-t",
            f"{duration:.6f}",
            "-c:v",
            "libx264",
            "-preset",
            preset,
            *(["-tune", tune] if tune else []),
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-color_primaries",
            "bt709",
            "-color_trc",
            "bt709",
            "-colorspace",
            "bt709",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-ar",
            "48000",
            "-ac",
            "2",
            "-movflags",
            "+faststart",
            str(output_video),
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Temporally conservative Real-ESRGAN/Lanczos upscale for PhotoDay v3."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio-from", type=Path, default=DEFAULT_AUDIO)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument(
        "--frame-dir", type=Path, default=PACKAGE_ROOT / "outputs" / "upscaled_frames"
    )
    parser.add_argument(
        "--source-frame-dir",
        type=Path,
        help="Optional directory containing lossless source_00001.png frames. "
        "Defaults to --frame-dir and extracts them from --input when absent.",
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--width", type=int, default=1080)
    parser.add_argument("--height", type=int, default=1920)
    parser.add_argument("--fps", type=int, default=24)
    parser.add_argument("--frame-count", type=int, default=240)
    parser.add_argument("--tile", type=int, default=256)
    parser.add_argument("--overlap", type=int, default=32)
    parser.add_argument(
        "--sr-blend",
        type=float,
        default=0.65,
        help="Real-ESRGAN share; the remainder is clean Lanczos (default 0.65).",
    )
    parser.add_argument("--crf", type=int, default=16)
    parser.add_argument("--preset", default="slow")
    parser.add_argument("--tune", default=None)
    parser.add_argument("--unsharp-radius", type=float, default=0.0)
    parser.add_argument("--unsharp-percent", type=int, default=0)
    parser.add_argument("--unsharp-threshold", type=int, default=2)
    parser.add_argument("--extract-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for required in (args.input, args.audio_from, args.model):
        if not required.is_file():
            raise FileNotFoundError(required)
    if not 0.0 <= args.sr_blend <= 1.0:
        raise ValueError("--sr-blend must be between 0 and 1")
    source_frame_dir = args.source_frame_dir or args.frame_dir
    extract_frames(args.input, source_frame_dir, args.frame_count)
    if args.extract_only:
        return
    if not torch.cuda.is_available() and args.device.startswith("cuda"):
        raise RuntimeError("CUDA requested but is not available")
    device = torch.device(args.device)
    model = load_upscaler(args.model, device)
    process_frames(
        source_frame_dir=source_frame_dir,
        output_frame_dir=args.frame_dir,
        model=model,
        device=device,
        comfy_root=args.comfy_root,
        frame_count=args.frame_count,
        width=args.width,
        height=args.height,
        tile=args.tile,
        overlap=args.overlap,
        sr_blend=args.sr_blend,
        unsharp_radius=args.unsharp_radius,
        unsharp_percent=args.unsharp_percent,
        unsharp_threshold=args.unsharp_threshold,
    )
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()
    encode(
        frame_dir=args.frame_dir,
        audio_from=args.audio_from,
        output_video=args.output,
        fps=args.fps,
        frame_count=args.frame_count,
        crf=args.crf,
        preset=args.preset,
        tune=args.tune,
    )


if __name__ == "__main__":
    main()
