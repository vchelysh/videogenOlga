from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
import uuid
from pathlib import Path

import requests


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMFY_ROOT = Path(r"C:\Users\Vadim\ComfyUI")
DEFAULT_BASE_URL = "http://127.0.0.1:8188"
SPEC_PATH = PACKAGE_ROOT / "prompts" / "generation_spec_v5.json"


def node(class_type: str, **inputs):
    return {"class_type": class_type, "inputs": inputs}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def load_scene(scene_id: str, take: int) -> tuple[dict, dict, str, int]:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    scene = spec["scenes"][scene_id]
    prompt_path = PACKAGE_ROOT / scene["prompt_file"]
    keyframe_path = PACKAGE_ROOT / scene["keyframe_file"]
    if not prompt_path.is_file():
        raise FileNotFoundError(prompt_path)
    if not keyframe_path.is_file():
        raise FileNotFoundError(keyframe_path)
    prompt = prompt_path.read_text(encoding="utf-8").strip()
    seed = int(scene["seed"]) + (take - 1) * 1009
    return spec, scene, prompt, seed


def build_graph(spec: dict, scene: dict, prompt: str, seed: int, scene_id: str, take: int) -> dict:
    models = spec["models"]
    input_name = f"h3_photoday_v5/scene_{scene_id}_start.png"
    prefix = f"minimax_h3_photoday_v5/scene_{scene_id}_take{take:02d}"
    return {
        "1": node("UNETLoader", unet_name=models["unet"], weight_dtype="default"),
        "2": node(
            "LoraLoaderModelOnly",
            model=["1", 0],
            lora_name=models["turbo_lora"],
            strength_model=float(models["turbo_strength"]),
        ),
        "3": node(
            "CLIPLoader",
            clip_name=models["text_encoder"],
            type="minimax",
            device="default",
        ),
        "4": node("VAELoader", vae_name=models["video_vae"]),
        "10": node("LoadImage", image=input_name),
        "20": node(
            "MiniMaxH3ImageToVideo",
            clip=["3", 0],
            vae=["4", 0],
            prompt=prompt,
            width=int(scene["width"]),
            height=int(scene["height"]),
            length=int(scene["length"]),
            first_frame=["10", 0],
        ),
        "30": node("BasicGuider", model=["2", 0], conditioning=["20", 0]),
        "31": node("RandomNoise", noise_seed=seed),
        "32": node("KSamplerSelect", sampler_name=spec["sampler"]),
        "33": node(
            "BasicScheduler",
            model=["2", 0],
            scheduler=spec["scheduler"],
            steps=int(spec["steps"]),
            denoise=float(spec["denoise"]),
        ),
        "34": node(
            "SamplerCustomAdvanced",
            noise=["31", 0],
            guider=["30", 0],
            sampler=["32", 0],
            sigmas=["33", 0],
            latent_image=["20", 1],
        ),
        "40": node("VAEDecode", samples=["34", 0], vae=["4", 0]),
        "42": node(
            "CreateVideo",
            images=["40", 0],
            fps=float(spec["fps"]),
            codec="none",
        ),
        "43": node(
            "SaveVideo",
            video=["42", 0],
            filename_prefix=prefix,
            format="mov",
            codec="prores",
        ),
    }


def prepare_input(comfy_root: Path, scene_id: str, scene: dict) -> Path:
    source = PACKAGE_ROOT / scene["keyframe_file"]
    target_dir = comfy_root / "input" / "h3_photoday_v5"
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"scene_{scene_id}_start.png"
    shutil.copy2(source, target)
    return target


def wait_for_completion(base_url: str, prompt_id: str, poll_seconds: int) -> tuple[dict, float]:
    started = time.time()
    while True:
        history = requests.get(f"{base_url}/history/{prompt_id}", timeout=60).json()
        if prompt_id in history:
            item = history[prompt_id]
            status = item["status"]["status_str"]
            elapsed = (time.time() - started) / 60
            print(f"finished {prompt_id}: {status} after {elapsed:.1f} min", flush=True)
            if status != "success":
                raise RuntimeError(item["status"])
            return item, elapsed
        queue = requests.get(f"{base_url}/queue", timeout=60).json()
        elapsed = (time.time() - started) / 60
        print(
            f"running {prompt_id}: {elapsed:.1f} min; "
            f"active={len(queue.get('queue_running', []))} "
            f"pending={len(queue.get('queue_pending', []))}",
            flush=True,
        )
        time.sleep(poll_seconds)


def copy_saved_video(item: dict, comfy_root: Path, scene_id: str, take: int, scene: dict) -> Path:
    output = item.get("outputs", {}).get("43", {})
    files = output.get("images", [])
    if not files:
        raise RuntimeError(f"No saved video metadata: {output}")
    metadata = files[0]
    source = comfy_root / "output" / metadata.get("subfolder", "") / metadata["filename"]
    if not source.is_file():
        raise FileNotFoundError(source)
    target = (
        PACKAGE_ROOT
        / "outputs"
        / "raw"
        / "v5"
        / f"PhotoDay_H3_v5_scene{scene_id}_take{take:02d}_{scene['width']}x{scene['height']}_{scene['length']}f.mov"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def write_manifest(
    spec: dict,
    scene: dict,
    scene_id: str,
    take: int,
    seed: int,
    graph: dict,
    prompt_id: str | None,
    elapsed_minutes: float | None,
    output: Path | None,
) -> Path:
    workflow_dir = PACKAGE_ROOT / "workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    workflow_path = workflow_dir / f"minimax_h3_v5_scene{scene_id}_take{take:02d}_api.json"
    workflow_path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "project": spec["project"],
        "strategy": spec["strategy"],
        "scene": scene_id,
        "take": take,
        "seed": seed,
        "width": scene["width"],
        "height": scene["height"],
        "length": scene["length"],
        "fps": spec["fps"],
        "steps": spec["steps"],
        "sampler": spec["sampler"],
        "scheduler": spec["scheduler"],
        "denoise": spec["denoise"],
        "models": spec["models"],
        "prompt_file": scene["prompt_file"],
        "keyframe_file": scene["keyframe_file"],
        "keyframe_sha256": sha256(PACKAGE_ROOT / scene["keyframe_file"]),
        "workflow_file": str(workflow_path.relative_to(PACKAGE_ROOT)).replace("\\", "/"),
        "prompt_id": prompt_id,
        "render_minutes": elapsed_minutes,
        "output": str(output.relative_to(PACKAGE_ROOT)).replace("\\", "/") if output else None,
        "output_sha256": sha256(output) if output else None,
    }
    manifest_path = workflow_dir / f"generation_manifest_v5_scene{scene_id}_take{take:02d}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate one isolated PhotoDay H3 v5 repair scene.")
    parser.add_argument("--scene", choices=("01", "03", "04"), required=True)
    parser.add_argument("--take", type=int, default=1)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.take < 1:
        raise ValueError("--take must be at least 1")
    spec, scene, prompt, seed = load_scene(args.scene, args.take)
    prepared = prepare_input(args.comfy_root, args.scene, scene)
    graph = build_graph(spec, scene, prompt, seed, args.scene, args.take)
    manifest_path = write_manifest(
        spec, scene, args.scene, args.take, seed, graph, None, None, None
    )
    print(f"prepared {prepared}", flush=True)
    print(f"exported {manifest_path}", flush=True)
    if args.prepare_only:
        return

    requests.get(f"{args.base_url}/system_stats", timeout=30).raise_for_status()
    requests.post(
        f"{args.base_url}/free",
        json={"unload_models": True, "free_memory": True},
        timeout=30,
    ).raise_for_status()
    response = requests.post(
        f"{args.base_url}/prompt",
        json={"prompt": graph, "client_id": str(uuid.uuid4())},
        timeout=120,
    )
    if not response.ok:
        print(response.text, flush=True)
        response.raise_for_status()
    prompt_id = response.json()["prompt_id"]
    print(f"started scene {args.scene} take {args.take:02d}: {prompt_id}", flush=True)
    item, elapsed = wait_for_completion(args.base_url, prompt_id, args.poll_seconds)
    target = copy_saved_video(item, args.comfy_root, args.scene, args.take, scene)
    write_manifest(
        spec, scene, args.scene, args.take, seed, graph, prompt_id, elapsed, target
    )
    print(f"copied scene master to {target}", flush=True)


if __name__ == "__main__":
    main()
