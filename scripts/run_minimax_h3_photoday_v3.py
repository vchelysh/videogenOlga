from __future__ import annotations

import argparse
import json
import shutil
import time
import uuid
from pathlib import Path

import requests


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_COMFY_ROOT = Path(r"C:\Users\Vadim\ComfyUI")
DEFAULT_BASE_URL = "http://127.0.0.1:8188"


def node(class_type: str, **inputs):
    return {"class_type": class_type, "inputs": inputs}


def load_inputs() -> tuple[dict, str]:
    spec = json.loads(
        (PACKAGE_ROOT / "prompts" / "generation_spec_v3.json").read_text(encoding="utf-8")
    )
    prompt = (PACKAGE_ROOT / "prompts" / "video_prompt_v3.txt").read_text(
        encoding="utf-8"
    ).strip()
    return spec, prompt


def build_graph(spec: dict, prompt: str) -> dict:
    models = spec["models"]
    graph = {
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
        "5": node("VAELoader", vae_name=models["audio_vae"]),
        "10": node("LoadImage", image="h3_photoday_v3/scene_01.png"),
        "11": node("LoadImage", image="h3_photoday_v3/scene_02.png"),
        "12": node("LoadImage", image="h3_photoday_v3/scene_03.png"),
        "13": node("LoadImage", image="h3_photoday_v3/scene_04.png"),
        "14": node("LoadImage", image="h3_photoday_v3/scene_05.png"),
        "20": node(
            "MiniMaxH3ImageToVideo",
            clip=["3", 0],
            vae=["4", 0],
            prompt=prompt,
            width=int(spec["width"]),
            height=int(spec["height"]),
            length=int(spec["length"]),
            first_frame=["10", 0],
            last_frame=["14", 0],
        ),
        "21": node(
            "MiniMaxH3AddGuide",
            positive=["20", 0],
            latent=["20", 1],
            vae=["4", 0],
            image=["11", 0],
            frame_idx=48,
        ),
        "22": node(
            "MiniMaxH3AddGuide",
            positive=["21", 0],
            latent=["20", 1],
            vae=["4", 0],
            image=["12", 0],
            frame_idx=96,
        ),
        "23": node(
            "MiniMaxH3AddGuide",
            positive=["22", 0],
            latent=["20", 1],
            vae=["4", 0],
            image=["13", 0],
            frame_idx=144,
        ),
        "24": node(
            "MiniMaxH3AddGuide",
            positive=["23", 0],
            latent=["20", 1],
            vae=["4", 0],
            image=["14", 0],
            frame_idx=192,
        ),
        "30": node("BasicGuider", model=["2", 0], conditioning=["24", 0]),
        "31": node("RandomNoise", noise_seed=int(spec["seed"])),
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
        "41": node("VAEDecodeAudio", samples=["34", 0], vae=["5", 0]),
        "42": node(
            "CreateVideo",
            images=["40", 0],
            audio=["41", 0],
            fps=float(spec["fps"]),
            codec="none",
        ),
        "43": node(
            "SaveVideo",
            video=["42", 0],
            filename_prefix="minimax_h3_photoday_v3/photoday_h3_dynamic_v3",
            format="mp4",
            codec="h264",
        ),
    }
    return graph


def prepare_inputs(comfy_root: Path) -> None:
    target = comfy_root / "input" / "h3_photoday_v3"
    target.mkdir(parents=True, exist_ok=True)
    for index in range(1, 6):
        name = f"scene_{index:02d}.png"
        source = PACKAGE_ROOT / "keyframes" / name
        if not source.is_file():
            raise FileNotFoundError(source)
        shutil.copy2(source, target / name)


def export_workflow(spec: dict, prompt: str, graph: dict) -> None:
    workflow_dir = PACKAGE_ROOT / "workflow"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    (workflow_dir / "minimax_h3_v3_api.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    manifest = dict(spec)
    manifest["prompt_file"] = "prompts/video_prompt_v3.txt"
    manifest["workflow_file"] = "workflow/minimax_h3_v3_api.json"
    (workflow_dir / "generation_manifest_v3.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def wait_for_completion(base_url: str, prompt_id: str, poll_seconds: int) -> dict:
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
            return item
        queue = requests.get(f"{base_url}/queue", timeout=60).json()
        elapsed = (time.time() - started) / 60
        print(
            f"running {prompt_id}: {elapsed:.1f} min; "
            f"active={len(queue.get('queue_running', []))} "
            f"pending={len(queue.get('queue_pending', []))}",
            flush=True,
        )
        time.sleep(poll_seconds)


def copy_saved_video(item: dict, comfy_root: Path) -> Path:
    save_output = item.get("outputs", {}).get("43", {})
    files = save_output.get("images", [])
    if not files:
        raise RuntimeError(f"No saved video metadata: {save_output}")
    metadata = files[0]
    source = comfy_root / "output" / metadata.get("subfolder", "") / metadata["filename"]
    if not source.is_file():
        raise FileNotFoundError(source)
    target = PACKAGE_ROOT / "outputs" / "raw" / "PhotoDay_H3_v3_raw_448x800_10.125s.mp4"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the continuous dynamic PhotoDay H3 v3 film.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--comfy-root", type=Path, default=DEFAULT_COMFY_ROOT)
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--poll-seconds", type=int, default=20)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    spec, prompt = load_inputs()
    prepare_inputs(args.comfy_root)
    graph = build_graph(spec, prompt)
    export_workflow(spec, prompt, graph)
    print("prepared continuous v3 graph", flush=True)
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
    print(f"started continuous v3: {prompt_id}", flush=True)
    item = wait_for_completion(args.base_url, prompt_id, args.poll_seconds)
    target = copy_saved_video(item, args.comfy_root)
    print(f"copied v3 raw master to {target}", flush=True)


if __name__ == "__main__":
    main()
