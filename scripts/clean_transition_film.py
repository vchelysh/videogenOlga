from __future__ import annotations

import argparse
import subprocess
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
DEFAULT_AUDIO = PACKAGE_ROOT / "references" / "PhotoDay_v1_motion_master.mp4"


def decode_rgb(path: Path, count: int) -> list[np.ndarray]:
    container = av.open(str(path))
    frames: list[np.ndarray] = []
    try:
        for frame in container.decode(video=0):
            frames.append(frame.to_ndarray(format="rgb24"))
            if len(frames) == count:
                break
    finally:
        container.close()
    if len(frames) != count:
        raise RuntimeError(f"Expected {count} frames, decoded {len(frames)}")
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
    print(f"loaded FILM model on {device} as {dtype}", flush=True)
    return model, dtype


def to_tensor(frame: np.ndarray, device: torch.device, dtype: torch.dtype) -> torch.Tensor:
    tensor = torch.from_numpy(frame.astype(np.float32) / 255.0)
    return tensor.permute(2, 0, 1).unsqueeze(0).to(device=device, dtype=dtype)


@torch.inference_mode()
def interpolate_2x(
    frames: list[np.ndarray], model, device: torch.device, dtype: torch.dtype
) -> list[np.ndarray]:
    output: list[np.ndarray] = []
    for index in range(len(frames) - 1):
        first = frames[index]
        second = frames[index + 1]
        image0 = to_tensor(first, device, dtype)
        image1 = to_tensor(second, device, dtype)
        midpoint = model(image0, image1, timestep=0.5)
        midpoint = midpoint[0].permute(1, 2, 0).float().clamp(0.0, 1.0).cpu()
        middle_array = (midpoint.numpy() * 255.0 + 0.5).astype(np.uint8)
        output.extend((first, middle_array))
        del image0, image1, midpoint
        print(f"FILM pair {index + 1:02d}/{len(frames) - 1:02d}", flush=True)
    output.append(frames[-1])
    return output


def save_source_frames(frames: list[np.ndarray], frame_dir: Path) -> None:
    frame_dir.mkdir(parents=True, exist_ok=True)
    for stale in frame_dir.glob("source_*.png"):
        stale.unlink()
    for index, frame in enumerate(frames, start=1):
        path = frame_dir / f"source_{index:05d}.png"
        Image.fromarray(frame, mode="RGB").save(path, format="PNG", optimize=False)
    print(f"wrote {len(frames)} corrected source frames to {frame_dir}", flush=True)


def encode_preview(
    frame_dir: Path, audio_from: Path, output: Path, fps: int, frame_count: int
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-framerate",
        str(fps),
        "-i",
        str(frame_dir / "source_%05d.png"),
        "-i",
        str(audio_from),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0?",
        "-frames:v",
        str(frame_count),
        "-t",
        f"{frame_count / fps:.6f}",
        "-c:v",
        "libx264",
        "-preset",
        "slow",
        "-crf",
        "12",
        "-pix_fmt",
        "yuv420p",
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
        str(output),
    ]
    subprocess.run(command, check=True)
    print(f"encoded corrected preview to {output}", flush=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove the generated flash/morph transition using only clean frames and FILM interpolation."
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--audio-from", type=Path, default=DEFAULT_AUDIO)
    parser.add_argument("--model", type=Path, default=DEFAULT_MODEL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument(
        "--frame-dir", type=Path, default=PACKAGE_ROOT / "outputs" / "upscaled_frames"
    )
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--fps", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    for required in (args.input, args.audio_from, args.model):
        if not required.is_file():
            raise FileNotFoundError(required)
    device = torch.device(args.device)
    if device.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")

    original = decode_rgb(args.input, 240)
    # Frames 144..166 are the complete clean champagne action. Frame 167 starts
    # the unwanted morph and frame 175 starts the severe hair/shoulder flare.
    clean_scene4 = original[144:167]
    # Two repeated settle frames make 25 inputs; 2x FILM yields 49 frames. Keep
    # the first 48, giving an exact 2.000-second scene without flare or morph.
    film_inputs = clean_scene4 + [clean_scene4[-1], clean_scene4[-1]]
    model, dtype = load_film(args.comfy_root, args.model, device)
    scene4 = interpolate_2x(film_inputs, model, device, dtype)[:48]
    del model
    if device.type == "cuda":
        torch.cuda.empty_cache()

    corrected = original[:144] + scene4 + original[192:240]
    if len(corrected) != 240:
        raise AssertionError(len(corrected))
    save_source_frames(corrected, args.frame_dir)
    encode_preview(args.frame_dir, args.audio_from, args.output, args.fps, 240)


if __name__ == "__main__":
    main()
