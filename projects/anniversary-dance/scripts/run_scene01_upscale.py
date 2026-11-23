from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
COMFY = Path(r"C:\Users\Vadim\ComfyUI")
RUN_ID = "scene-01-upscale-realesrgan-x2-v1"
SOURCE = (
    PROJECT
    / "workspace"
    / "runs"
    / "scene-01-repair-fl2va-v2"
    / "outputs"
    / "scene-01-repair-fl2va-v2_00001__review.mp4"
)
INPUT_NAME = "anniversary-dance/scene-01-repair-fl2va-v2-review.mp4"
RUN_DIR = PROJECT / "workspace" / "runs" / RUN_ID
OUTPUTS = RUN_DIR / "outputs"
WORKFLOW = RUN_DIR / "workflow_api.json"
MANIFEST = RUN_DIR / "manifest.json"

sys.path.insert(0, r"C:\Users\Vadim\.agents\skills\comfyui")
import comfy_client as comfy  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict:
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


def media_record(path: Path) -> dict:
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries",
            "stream=codec_name,width,height,pix_fmt,avg_frame_rate,nb_frames,duration",
            "-show_entries", "format=duration,size", "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return {
        "path": str(path.relative_to(PROJECT)).replace("\\", "/"),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "probe": json.loads(probe.stdout),
    }


def make_delivery_mp4(source: Path) -> Path:
    target = source.with_name(f"{source.stem}_delivery.mp4")
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
            "-map", "0:v:0", "-vf", "scale=1080:1440:flags=lanczos",
            "-c:v", "libx264", "-preset", "slow", "-crf", "17",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-r", "24", "-an",
            str(target),
        ],
        check=True,
    )
    return target


def is_target_size(path: Path) -> bool:
    probe = subprocess.run(
        [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width,height", "-of", "json", str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    stream = json.loads(probe.stdout)["streams"][0]
    return stream["width"] == 1080 and stream["height"] == 1440


def main() -> None:
    if not SOURCE.is_file():
        raise FileNotFoundError(SOURCE)
    input_path = COMFY / "input" / INPUT_NAME
    input_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE, input_path)

    workflow = read_json(
        PROJECT / "workflow" / "scene-01-upscale-realesrgan-x2-v1-api.template.json"
    )
    write_json(WORKFLOW, workflow)
    manifest = {
        "run_id": RUN_ID,
        "status": "prepared",
        "created_utc": utc_now(),
        "source": {
            "path": str(SOURCE.relative_to(PROJECT)).replace("\\", "/"),
            "sha256": sha256(SOURCE),
        },
        "model": "RealESRGAN_x2plus.pth",
        "workflow": str(WORKFLOW.relative_to(PROJECT)).replace("\\", "/"),
        "target": {"width": 1080, "height": 1440, "fps": 24, "frames": 158},
    }
    write_json(MANIFEST, manifest)

    prompt_id = comfy.queue(workflow)
    manifest.update({"status": "queued", "prompt_id": prompt_id, "submitted_utc": utc_now()})
    write_json(MANIFEST, manifest)
    print(f"PROMPT_ID={prompt_id}", flush=True)

    started = time.time()
    last_report = 0.0
    deadline = started + 3600
    try:
        while time.time() < deadline:
            history = comfy._get(f"/history/{prompt_id}")
            record = history.get(prompt_id)
            if record:
                status = record.get("status") or {}
                if status.get("status_str") == "error":
                    raise RuntimeError(json.dumps(status, ensure_ascii=False))
                if record.get("outputs"):
                    break
            now = time.time()
            if now - last_report >= 20:
                queue = comfy._get("/queue")
                print(
                    f"WAIT elapsed={int(now - started)}s "
                    f"running={len(queue.get('queue_running') or [])} "
                    f"pending={len(queue.get('queue_pending') or [])}",
                    flush=True,
                )
                last_report = now
            time.sleep(2)
        else:
            raise TimeoutError(f"prompt {prompt_id} exceeded 3600 seconds")

        saved = [Path(p) for p in comfy.download_outputs(record, str(OUTPUTS))]
        if not saved:
            raise RuntimeError("ComfyUI returned no downloadable output")
        upscaled = [path for path in saved if is_target_size(path)]
        if not upscaled:
            raise RuntimeError("ComfyUI returned no 1080x1440 upscale output")
        deliveries = [make_delivery_mp4(path) for path in upscaled]
        manifest.update(
            {
                "status": "completed_unreviewed",
                "completed_utc": utc_now(),
                "runtime_seconds": round(time.time() - started, 3),
                "outputs": [media_record(path) for path in saved],
                "delivery_outputs": [media_record(path) for path in deliveries],
                "comfy_status": record.get("status"),
            }
        )
        write_json(MANIFEST, manifest)
        for path in deliveries:
            print(f"DELIVERY_MP4={path}", flush=True)
    except Exception as exc:
        manifest.update({"status": "failed", "failed_utc": utc_now(), "error": repr(exc)})
        write_json(MANIFEST, manifest)
        raise


if __name__ == "__main__":
    main()
