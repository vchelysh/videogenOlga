from __future__ import annotations

import hashlib
import json
import shutil
from copy import deepcopy
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RUN_ID = "scene-01-repair-fl2va-v2"
SEED = 24112402

COMFY = Path(r"C:\Users\Vadim\ComfyUI")
TEMPLATE = Path(
    r"C:\Users\Vadim\comfyui-agent-kit-data\workflow_templates\templates"
    r"\video_minimax_h3_i2v.json"
)
FIRST_NAME = "anniversary-dance/scene-01-first-v1.png"
LAST_NAME = "anniversary-dance/scene-01-last-v1.png"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> None:
    prompt = (PROJECT / "prompts" / "scene-01-h3-prompt-v2.txt").read_text(
        encoding="utf-8"
    ).strip()
    first_anchor = PROJECT / "workspace" / "anchors" / "scene-01-first-v1.png"
    last_anchor = PROJECT / "workspace" / "anchors" / "scene-01-last-v1.png"
    for source, relative_name in (
        (first_anchor, FIRST_NAME),
        (last_anchor, LAST_NAME),
    ):
        if not source.is_file():
            raise FileNotFoundError(source)
        target = COMFY / "input" / relative_name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    run_dir = PROJECT / "workspace" / "runs" / RUN_ID
    api = load_json(
        PROJECT / "workflow" / "scene-01-repair-fl2va-v2-api.template.json"
    )
    api["20"]["inputs"]["prompt"] = prompt
    api["31"]["inputs"]["noise_seed"] = SEED
    api_path = run_dir / "workflow_api.json"
    write_json(api_path, api)

    gui = load_json(TEMPLATE)
    first_node = None
    subgraph_node = None
    for node in gui["nodes"]:
        if node["id"] == 114:
            first_node = node
            node["widgets_values"][0] = FIRST_NAME
        elif node["id"] == 115:
            node["widgets_values"] = ["3:4 (Portrait Standard)", 0.44, 32]
        elif node["id"] == 105:
            subgraph_node = node
            node["widgets_values"] = [
                prompt,
                576,
                768,
                6.583333333333333,
                SEED,
                "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
                "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
                "minimax_h3_video_vae_int8_convrot.safetensors",
                "minimax_h3_audio_vae_fp32.safetensors",
                False,
                "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
                0.0,
                20,
            ]
        elif node["id"] == 92:
            node["widgets_values"] = [
                f"anniversary-dance/{RUN_ID}",
                "mov",
                "prores",
            ]

    if first_node is None or subgraph_node is None:
        raise RuntimeError("official H3 template structure changed")
    last_node = deepcopy(first_node)
    last_node["id"] = 121
    last_node["pos"] = [-1610, 4200]
    last_node["widgets_values"][0] = LAST_NAME
    last_node["outputs"][0]["links"] = [246]
    gui["nodes"].append(last_node)
    subgraph_node["inputs"][1]["link"] = 246
    gui["links"].append([246, 121, 0, 105, 1, "IMAGE"])
    gui["last_node_id"] = max(int(gui.get("last_node_id", 0)), 121)
    gui["last_link_id"] = max(int(gui.get("last_link_id", 0)), 246)

    gui_path = PROJECT / "workflow" / f"{RUN_ID}-gui.json"
    write_json(gui_path, gui)
    comfy_gui = COMFY / "user" / "default" / "workflows" / f"{RUN_ID}.json"
    write_json(comfy_gui, gui)

    manifest = {
        "run_id": RUN_ID,
        "status": "prepared",
        "mode": "fl2va_first_and_last_frame",
        "repair_targets": [
            "engaged male gaze from first live frame",
            "stable male and female hair geometry without shimmer",
            "frozen background guests",
        ],
        "seed": SEED,
        "width": 576,
        "height": 768,
        "frames": 158,
        "fps": 24,
        "steps": 20,
        "turbo_lora": None,
        "sampler": "res_multistep",
        "scheduler": "simple",
        "prompt": "prompts/scene-01-h3-prompt-v2.txt",
        "anchors": {
            "first": {
                "path": "workspace/anchors/scene-01-first-v1.png",
                "sha256": sha256(first_anchor),
            },
            "last": {
                "path": "workspace/anchors/scene-01-last-v1.png",
                "sha256": sha256(last_anchor),
                "source": "scene-01-proof-i2v-v1 frame 84",
            },
        },
        "api_workflow": str(api_path.relative_to(PROJECT)).replace("\\", "/"),
        "gui_workflow": str(gui_path.relative_to(PROJECT)).replace("\\", "/"),
        "comfy_gui_workflow": str(comfy_gui),
        "required_review_format": {
            "container": "mp4",
            "codec": "h264",
            "pixel_format": "yuv420p",
            "faststart": True,
        },
    }
    write_json(run_dir / "manifest.json", manifest)
    print(api_path)
    print(gui_path)
    print(comfy_gui)


if __name__ == "__main__":
    main()
