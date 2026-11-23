from __future__ import annotations

import json
import shutil
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RUN_ID = "scene-01-proof-i2v-v1"
SEED = 24112401

COMFY = Path(r"C:\Users\Vadim\ComfyUI")
TEMPLATE = Path(
    r"C:\Users\Vadim\comfyui-agent-kit-data\workflow_templates\templates"
    r"\video_minimax_h3_i2v.json"
)
COMFY_INPUT_NAME = "anniversary-dance/scene-01-first-v1.png"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> None:
    prompt = (
        PROJECT / "prompts" / "scene-01-h3-prompt-proof-i2v-v1.txt"
    ).read_text(encoding="utf-8").strip()
    first_anchor = PROJECT / "workspace" / "anchors" / "scene-01-first-v1.png"
    if not first_anchor.is_file():
        raise FileNotFoundError(first_anchor)

    comfy_input = COMFY / "input" / COMFY_INPUT_NAME
    comfy_input.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(first_anchor, comfy_input)

    run_dir = PROJECT / "workspace" / "runs" / RUN_ID
    api = load_json(
        PROJECT / "workflow" / "scene-01-proof-i2v-v1-api.template.json"
    )
    api["20"]["inputs"]["prompt"] = prompt
    api["31"]["inputs"]["noise_seed"] = SEED
    api_path = run_dir / "workflow_api.json"
    write_json(api_path, api)

    gui = load_json(TEMPLATE)
    for node in gui["nodes"]:
        if node["id"] == 114:
            node["widgets_values"][0] = COMFY_INPUT_NAME
        elif node["id"] == 115:
            node["widgets_values"] = ["3:4 (Portrait Standard)", 0.31, 32]
        elif node["id"] == 105:
            node["widgets_values"] = [
                prompt,
                480,
                640,
                6.583333333333333,
                SEED,
                "minimax_h3_fl2va_pruned_int8_convrot.safetensors",
                "qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
                "minimax_h3_video_vae_int8_convrot.safetensors",
                "minimax_h3_audio_vae_fp32.safetensors",
                False,
                "minimax_h3_fl2v_turbo_8step_v1.0_comfyui_bf16.safetensors",
                1.0,
                8,
            ]
        elif node["id"] == 92:
            node["widgets_values"] = [
                f"anniversary-dance/{RUN_ID}",
                "mov",
                "prores",
            ]

    gui_path = PROJECT / "workflow" / f"{RUN_ID}-gui.json"
    write_json(gui_path, gui)
    comfy_gui = COMFY / "user" / "default" / "workflows" / f"{RUN_ID}.json"
    write_json(comfy_gui, gui)

    manifest = {
        "run_id": RUN_ID,
        "status": "prepared",
        "mode": "i2va_first_frame_proof",
        "seed": SEED,
        "width": 480,
        "height": 640,
        "frames": 158,
        "fps": 24,
        "steps": 8,
        "sampler": "res_multistep",
        "scheduler": "simple",
        "prompt": "prompts/scene-01-h3-prompt-proof-i2v-v1.txt",
        "first_anchor": "workspace/anchors/scene-01-first-v1.png",
        "api_workflow": str(api_path.relative_to(PROJECT)).replace("\\", "/"),
        "gui_workflow": str(gui_path.relative_to(PROJECT)).replace("\\", "/"),
        "comfy_gui_workflow": str(comfy_gui),
    }
    write_json(run_dir / "manifest.json", manifest)
    print(api_path)
    print(gui_path)
    print(comfy_gui)


if __name__ == "__main__":
    main()
