from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RUN_ID = "scene-01-repair-fl2va-v2"
RUN_DIR = PROJECT / "workspace" / "runs" / RUN_ID
WORKFLOW = RUN_DIR / "workflow_api.json"
MANIFEST = RUN_DIR / "manifest.json"
OUTPUTS = RUN_DIR / "outputs"

sys.path.insert(0, r"C:\Users\Vadim\.agents\skills\comfyui")
import comfy_client as comfy  # noqa: E402


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
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
            "ffprobe",
            "-v",
            "error",
            "-select_streams",
            "v:0",
            "-show_entries",
            "stream=codec_name,width,height,pix_fmt,avg_frame_rate,nb_frames,duration",
            "-show_entries",
            "format=duration,size",
            "-of",
            "json",
            str(path),
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


def make_review_mp4(source: Path) -> Path:
    review = source.with_name(f"{source.stem}_review.mp4")
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-map",
            "0:v:0",
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            "-r",
            "24",
            "-an",
            str(review),
        ],
        check=True,
    )
    return review


def main() -> None:
    workflow = read_json(WORKFLOW)
    manifest = read_json(MANIFEST)
    prompt_id = comfy.queue(workflow)
    manifest.update(
        {
            "status": "queued",
            "prompt_id": prompt_id,
            "submitted_utc": utc_now(),
        }
    )
    write_json(MANIFEST, manifest)
    print(f"PROMPT_ID={prompt_id}", flush=True)

    deadline = time.time() + 5400
    started = time.time()
    last_report = 0.0
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
            if now - last_report >= 30:
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
            raise TimeoutError(f"prompt {prompt_id} exceeded 5400 seconds")

        saved = [Path(p) for p in comfy.download_outputs(record, str(OUTPUTS))]
        reviews = [make_review_mp4(path) for path in saved]
        manifest.update(
            {
                "status": "completed_unreviewed",
                "completed_utc": utc_now(),
                "runtime_seconds": round(time.time() - started, 3),
                "outputs": [media_record(path) for path in saved],
                "review_outputs": [media_record(path) for path in reviews],
                "comfy_status": record.get("status"),
            }
        )
        write_json(MANIFEST, manifest)
        for path in saved:
            print(f"MEZZANINE={path}", flush=True)
        for path in reviews:
            print(f"REVIEW_MP4={path}", flush=True)
    except Exception as exc:
        manifest.update(
            {
                "status": "failed",
                "failed_utc": utc_now(),
                "error": repr(exc),
            }
        )
        write_json(MANIFEST, manifest)
        raise


if __name__ == "__main__":
    main()
