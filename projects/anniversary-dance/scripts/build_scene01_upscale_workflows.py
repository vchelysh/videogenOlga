from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
COMFY = Path(r"C:\Users\Vadim\ComfyUI")
RUN_ID = "scene-01-upscale-realesrgan-x2-v1"
INPUT_NAME = "anniversary-dance/scene-01-repair-fl2va-v2-review.mp4"

sys.path.insert(0, r"C:\Users\Vadim\.agents\skills\comfyui")
from workflow_layout import auto_layout, fit_group, inspect  # noqa: E402


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def port(name: str, kind: str, link: int | None = None, widget: bool = False) -> dict:
    value = {"name": name, "type": kind, "link": link}
    if widget:
        value["widget"] = {"name": name}
    return value


def output(name: str, kind: str, links: list[int]) -> dict:
    return {"name": name, "type": kind, "links": links}


def node(
    node_id: int,
    node_type: str,
    order: int,
    inputs: list[dict],
    outputs: list[dict],
    widgets: list,
) -> dict:
    return {
        "id": node_id,
        "type": node_type,
        "pos": [0, 0],
        "size": [320, 120],
        "flags": {},
        "order": order,
        "mode": 0,
        "inputs": inputs,
        "outputs": outputs,
        "properties": {"cnr_id": "comfy-core", "Node name for S&R": node_type},
        "widgets_values": widgets,
    }


def main() -> None:
    source = (
        PROJECT
        / "workspace"
        / "runs"
        / "scene-01-repair-fl2va-v2"
        / "outputs"
        / "scene-01-repair-fl2va-v2_00001__review.mp4"
    )
    if not source.is_file():
        raise FileNotFoundError(source)
    comfy_input = COMFY / "input" / INPUT_NAME
    comfy_input.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, comfy_input)

    workflow = {
        "last_node_id": 7,
        "last_link_id": 6,
        "nodes": [
            node(1, "LoadVideo", 0, [port("file", "COMBO", widget=True)], [output("VIDEO", "VIDEO", [1])], [INPUT_NAME]),
            node(2, "GetVideoComponents", 1, [port("video", "VIDEO", 1)], [output("images", "IMAGE", [2]), output("audio", "AUDIO", []), output("fps", "FLOAT", []), output("bit_depth", "COMBO", []), output("color_space", "COMBO", [])], []),
            node(3, "UpscaleModelLoader", 2, [port("model_name", "COMBO", widget=True)], [output("UPSCALE_MODEL", "UPSCALE_MODEL", [3])], ["RealESRGAN_x2plus.pth"]),
            node(4, "ImageUpscaleWithModel", 3, [port("upscale_model", "UPSCALE_MODEL", 3), port("image", "IMAGE", 2)], [output("IMAGE", "IMAGE", [4])], []),
            node(5, "ImageScale", 4, [port("image", "IMAGE", 4), port("upscale_method", "COMBO", widget=True), port("width", "INT", widget=True), port("height", "INT", widget=True), port("crop", "COMBO", widget=True)], [output("IMAGE", "IMAGE", [5])], ["lanczos", 1080, 1440, "disabled"]),
            node(6, "CreateVideo", 5, [port("images", "IMAGE", 5), port("fps", "FLOAT", widget=True), port("bit_depth", "COMBO", widget=True), port("color_space", "COMBO", widget=True), port("chroma_subsampling", "COMBO", widget=True), port("codec", "COMBO", widget=True)], [output("VIDEO", "VIDEO", [6])], [24, 8, "sRGB", "420", "none"]),
            node(7, "SaveVideo", 6, [port("video", "VIDEO", 6), port("filename_prefix", "STRING", widget=True), port("format", "COMFY_DYNAMICCOMBO_V3", widget=True), port("codec", "COMFY_DYNAMICCOMBO_V3", widget=True)], [output("video", "VIDEO", [])], [f"anniversary-dance/{RUN_ID}", "mp4", "h264"]),
        ],
        "links": [
            [1, 1, 0, 2, 0, "VIDEO"],
            [2, 2, 0, 4, 1, "IMAGE"],
            [3, 3, 0, 4, 0, "UPSCALE_MODEL"],
            [4, 4, 0, 5, 0, "IMAGE"],
            [5, 5, 0, 6, 0, "IMAGE"],
            [6, 6, 0, 7, 0, "VIDEO"],
        ],
        "groups": [],
        "config": {},
        "extra": {},
        "version": 0.4,
    }
    auto_layout(workflow)
    fit_group(workflow, "Anniversary dance: temporal-safe 1080x1440 upscale")
    report = inspect(workflow)
    if report["overlaps"] or report["crossings"]:
        raise RuntimeError(report)

    project_path = PROJECT / "workflow" / f"{RUN_ID}-gui.json"
    comfy_path = COMFY / "user" / "default" / "workflows" / f"{RUN_ID}.json"
    write_json(project_path, workflow)
    write_json(comfy_path, workflow)
    print(report["summary"])
    print(project_path)
    print(comfy_path)


if __name__ == "__main__":
    main()
