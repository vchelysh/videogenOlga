from __future__ import annotations

import gc
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from spandrel import ImageModelDescriptor, ModelLoader


ROOT = Path(__file__).resolve().parents[1]
COMFY_ROOT = Path(r"C:\Users\Vadim\ComfyUI")
FRAME_DIR = ROOT / "outputs" / "upscaled_frames"
OUT = ROOT / "review" / "upscale_v4_tests"
MODEL_DIR = COMFY_ROOT / "models" / "upscale_models"
FRAME_NUMBERS = (72, 110, 160, 210)
WIDTH = 1080
HEIGHT = 1920

MODELS = {
    "x4plus": MODEL_DIR / "RealESRGAN_x4plus.pth",
    "x2plus": MODEL_DIR / "RealESRGAN_x2plus.pth",
    "general_x4v3": MODEL_DIR / "realesr-general-x4v3.pth",
}

VARIANT_ORDER = (
    "current_v3_65x4_35lanczos",
    "lanczos_unsharp",
    "x4plus_full_unsharp",
    "x4plus_85_lanczos15",
    "x2plus_full_unsharp",
    "x2plus_85_lanczos15",
    "general_x4v3_unsharp",
)


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


def load_model(path: Path, device: torch.device) -> ImageModelDescriptor:
    descriptor = ModelLoader().load_from_file(path).eval()
    if not isinstance(descriptor, ImageModelDescriptor):
        raise TypeError(f"Unsupported model descriptor: {type(descriptor)!r}")
    descriptor = descriptor.to(device)
    print(f"loaded {path.name}; scale={descriptor.scale}", flush=True)
    return descriptor


@torch.inference_mode()
def upscale(
    source: Image.Image,
    model: ImageModelDescriptor,
    device: torch.device,
    tile: int = 256,
    overlap: int = 32,
) -> Image.Image:
    if str(COMFY_ROOT) not in sys.path:
        sys.path.insert(0, str(COMFY_ROOT))
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
    return Image.fromarray((result.numpy() * 255.0 + 0.5).astype(np.uint8), "RGB")


def sharpen(image: Image.Image, radius: float, percent: int, threshold: int) -> Image.Image:
    return image.filter(
        ImageFilter.UnsharpMask(radius=radius, percent=percent, threshold=threshold)
    )


def edge_metrics(image: Image.Image) -> dict[str, float]:
    gray = np.asarray(image.convert("L"), dtype=np.float32) / 255.0
    gx = np.diff(gray, axis=1)
    gy = np.diff(gray, axis=0)
    tenengrad = float((np.mean(gx * gx) + np.mean(gy * gy)) * 1_000_000)
    core = gray[1:-1, 1:-1]
    lap = (
        -4.0 * core
        + gray[1:-1, :-2]
        + gray[1:-1, 2:]
        + gray[:-2, 1:-1]
        + gray[2:, 1:-1]
    )
    return {
        "tenengrad_x1e6": tenengrad,
        "laplacian_variance_x1e6": float(np.var(lap) * 1_000_000),
    }


def label_tile(image: Image.Image, label: str) -> Image.Image:
    tile = image.copy()
    draw = ImageDraw.Draw(tile)
    font = ImageFont.load_default(size=22)
    box = draw.textbbox((0, 0), label, font=font)
    pad = 8
    draw.rectangle(
        (0, 0, box[2] - box[0] + pad * 2, box[3] - box[1] + pad * 2),
        fill=(0, 0, 0),
    )
    draw.text((pad, pad), label, fill=(255, 255, 255), font=font)
    return tile


def make_sheet(
    paths: list[Path],
    output: Path,
    crop_box: tuple[int, int, int, int] | None = None,
) -> None:
    tiles = []
    for path in paths:
        with Image.open(path) as loaded:
            image = loaded.convert("RGB")
        if crop_box is not None:
            image = image.crop(crop_box)
        image.thumbnail((480, 720), Image.Resampling.LANCZOS)
        tiles.append(label_tile(image, path.parent.name))
    width = sum(tile.width for tile in tiles)
    height = max(tile.height for tile in tiles)
    sheet = Image.new("RGB", (width, height), "black")
    x = 0
    for tile in tiles:
        sheet.paste(tile, (x, 0))
        x += tile.width
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output, quality=96, subsampling=0)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    device = torch.device("cuda")
    sources: dict[int, Image.Image] = {}
    lanczos: dict[int, Image.Image] = {}
    metrics: dict[str, dict[str, dict[str, float]]] = {}

    for number in FRAME_NUMBERS:
        with Image.open(FRAME_DIR / f"source_{number:05d}.png") as loaded:
            source = loaded.convert("RGB")
        sources[number] = source
        base = cover_crop(source, WIDTH, HEIGHT)
        lanczos[number] = base

        current_path = FRAME_DIR / f"upscaled_{number:05d}.png"
        current_out = OUT / VARIANT_ORDER[0] / f"frame_{number:05d}.png"
        current_out.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(current_path) as loaded:
            loaded.convert("RGB").save(current_out)

        direct = sharpen(base, radius=0.8, percent=95, threshold=2)
        direct_out = OUT / VARIANT_ORDER[1] / f"frame_{number:05d}.png"
        direct_out.parent.mkdir(parents=True, exist_ok=True)
        direct.save(direct_out)

    for model_name, model_path in MODELS.items():
        model = load_model(model_path, device)
        for number in FRAME_NUMBERS:
            source = sources[number]
            ai_full = upscale(source, model, device)
            ai_target = cover_crop(ai_full, WIDTH, HEIGHT)

            if model_name == "x4plus":
                full = sharpen(ai_target, radius=0.65, percent=75, threshold=2)
                blend = Image.blend(lanczos[number], ai_target, 0.85)
                blend = sharpen(blend, radius=0.65, percent=70, threshold=2)
                outputs = {
                    "x4plus_full_unsharp": full,
                    "x4plus_85_lanczos15": blend,
                }
            elif model_name == "x2plus":
                full = sharpen(ai_target, radius=0.7, percent=90, threshold=2)
                blend = Image.blend(lanczos[number], ai_target, 0.85)
                blend = sharpen(blend, radius=0.7, percent=85, threshold=2)
                outputs = {
                    "x2plus_full_unsharp": full,
                    "x2plus_85_lanczos15": blend,
                }
            else:
                outputs = {
                    "general_x4v3_unsharp": sharpen(
                        ai_target, radius=0.6, percent=65, threshold=2
                    )
                }

            for variant, image in outputs.items():
                path = OUT / variant / f"frame_{number:05d}.png"
                path.parent.mkdir(parents=True, exist_ok=True)
                image.save(path)
            print(f"{model_name}: frame {number}", flush=True)

        del model
        gc.collect()
        torch.cuda.empty_cache()

    crop_boxes = {
        72: (0, 320, 1080, 1400),
        110: (250, 80, 1030, 860),
        160: (180, 160, 1000, 980),
        210: (0, 80, 900, 980),
    }
    for number in FRAME_NUMBERS:
        paths = [OUT / name / f"frame_{number:05d}.png" for name in VARIANT_ORDER]
        make_sheet(paths, OUT / f"frame_{number:05d}_full_comparison.jpg")
        make_sheet(
            paths,
            OUT / f"frame_{number:05d}_detail_comparison.jpg",
            crop_box=crop_boxes[number],
        )

        metrics[str(number)] = {}
        for path in paths:
            with Image.open(path) as loaded:
                image = loaded.convert("RGB")
            crop = image.crop(crop_boxes[number])
            metrics[str(number)][path.parent.name] = edge_metrics(crop)

    (OUT / "sharpness_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    print(f"wrote comparisons to {OUT}", flush=True)


if __name__ == "__main__":
    main()
