from __future__ import annotations

import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
RUN_ID = "scene-01-proof-i2v-v1"
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

    deadline = time.time() + 3600
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
                running = len(queue.get("queue_running") or [])
                pending = len(queue.get("queue_pending") or [])
                print(
                    f"WAIT elapsed={int(now - (deadline - 3600))}s "
                    f"running={running} pending={pending}",
                    flush=True,
                )
                last_report = now
            time.sleep(2)
        else:
            raise TimeoutError(f"prompt {prompt_id} exceeded 3600 seconds")

        saved = [Path(p) for p in comfy.download_outputs(record, str(OUTPUTS))]
        manifest.update(
            {
                "status": "completed_unreviewed",
                "completed_utc": utc_now(),
                "outputs": [
                    {
                        "path": str(path.relative_to(PROJECT)).replace("\\", "/"),
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path),
                    }
                    for path in saved
                ],
                "comfy_status": record.get("status"),
            }
        )
        write_json(MANIFEST, manifest)
        for path in saved:
            print(f"OUTPUT={path}", flush=True)
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
