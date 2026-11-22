from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
V3_DIR = ROOT / "outputs" / "upscaled_frames"
V4_DIR = ROOT / "outputs" / "upscaled_frames_v4_sharp"
OUT = ROOT / "review" / "upscale_v4_final"
FRAME_COUNT = 240
HAIR_RANGE = range(193, 241)
HAIR_CROP = (0, 80, 900, 980)


def gray(path: Path, crop: tuple[int, int, int, int] | None = None) -> np.ndarray:
    with Image.open(path) as loaded:
        image = loaded.convert("L")
    if crop is not None:
        image = image.crop(crop)
    return np.asarray(image, dtype=np.float32) / 255.0


def edge_metrics(array: np.ndarray) -> tuple[float, float]:
    gx = np.diff(array, axis=1)
    gy = np.diff(array, axis=0)
    tenengrad = float((np.mean(gx * gx) + np.mean(gy * gy)) * 1_000_000)
    core = array[1:-1, 1:-1]
    lap = (
        -4.0 * core
        + array[1:-1, :-2]
        + array[1:-1, 2:]
        + array[:-2, 1:-1]
        + array[2:, 1:-1]
    )
    return tenengrad, float(np.var(lap) * 1_000_000)


def highpass(array: np.ndarray) -> np.ndarray:
    image = Image.fromarray((array * 255.0 + 0.5).astype(np.uint8), "L")
    low = np.asarray(image.filter(ImageFilter.GaussianBlur(1.0)), dtype=np.float32) / 255.0
    return array - low


def summarize(values: list[float]) -> dict[str, float]:
    data = np.asarray(values, dtype=np.float64)
    return {
        "mean": float(np.mean(data)),
        "median": float(np.median(data)),
        "min": float(np.min(data)),
        "max": float(np.max(data)),
        "std": float(np.std(data)),
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, float | int]] = []
    full: dict[str, dict[str, list[float]]] = {
        "v3": {"tenengrad": [], "laplacian": []},
        "v4": {"tenengrad": [], "laplacian": []},
    }

    for index in range(1, FRAME_COUNT + 1):
        record: dict[str, float | int] = {"frame": index}
        for label, directory in (("v3", V3_DIR), ("v4", V4_DIR)):
            array = gray(directory / f"upscaled_{index:05d}.png")
            tenengrad, laplacian = edge_metrics(array)
            full[label]["tenengrad"].append(tenengrad)
            full[label]["laplacian"].append(laplacian)
            record[f"{label}_tenengrad"] = tenengrad
            record[f"{label}_laplacian"] = laplacian
        rows.append(record)

    temporal: dict[str, dict[str, float]] = {}
    for label, directory in (("v3", V3_DIR), ("v4", V4_DIR)):
        normalized_changes: list[float] = []
        edge_energy: list[float] = []
        previous: np.ndarray | None = None
        previous_energy: float | None = None
        for index in HAIR_RANGE:
            array = gray(directory / f"upscaled_{index:05d}.png", HAIR_CROP)
            hp = highpass(array)
            energy = float(np.mean(np.abs(hp)))
            edge_energy.append(energy)
            if previous is not None and previous_energy is not None:
                denominator = max((energy + previous_energy) * 0.5, 1e-9)
                normalized_changes.append(float(np.mean(np.abs(hp - previous)) / denominator))
            previous = hp
            previous_energy = energy
        temporal[label] = {
            "normalized_highpass_temporal_change_mean": float(
                np.mean(normalized_changes)
            ),
            "normalized_highpass_temporal_change_p95": float(
                np.percentile(normalized_changes, 95)
            ),
            "hair_highpass_energy_mean": float(np.mean(edge_energy)),
            "hair_highpass_energy_cv": float(np.std(edge_energy) / np.mean(edge_energy)),
        }

    summary = {
        "full_frame": {
            label: {
                metric: summarize(values)
                for metric, values in metrics.items()
            }
            for label, metrics in full.items()
        },
        "ratios_v4_over_v3": {
            metric: float(
                np.mean(full["v4"][metric]) / np.mean(full["v3"][metric])
            )
            for metric in ("tenengrad", "laplacian")
        },
        "final_hair_temporal_stability": temporal,
        "hair_crop": HAIR_CROP,
        "hair_frames": "193-240",
    }

    with (OUT / "per_frame_sharpness.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (OUT / "sharpness_temporal_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
