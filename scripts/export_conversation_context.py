from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_THREAD_ID = "01a1ff14-0f52-7382-899b-5f54bc2f1ef9"
DEFAULT_ROLLOUT = Path(
    r"C:\Users\Vadim\.codex\sessions\2026\11\21\rollout-2026-11-21T19-07-47-01a1ff14-0f52-7382-899b-5f54bc2f1ef9.jsonl"
)
PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def extract_text(content: object) -> str:
    if not isinstance(content, list):
        return ""
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") in {"input_text", "output_text", "text"}:
            text = item.get("text")
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())
    return "\n\n".join(parts)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export only the user-visible user/assistant transcript from a Codex rollout."
    )
    parser.add_argument("--rollout", type=Path, default=DEFAULT_ROLLOUT)
    parser.add_argument(
        "--output",
        type=Path,
        default=PACKAGE_ROOT / "CONVERSATION_TRANSCRIPT.md",
    )
    parser.add_argument("--thread-id", default=DEFAULT_THREAD_ID)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.rollout.is_file():
        raise FileNotFoundError(args.rollout)

    messages: list[tuple[str, str, str, str]] = []
    with args.rollout.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if event.get("type") != "response_item":
                continue
            payload = event.get("payload")
            if not isinstance(payload, dict) or payload.get("type") != "message":
                continue
            role = payload.get("role")
            if role not in {"user", "assistant"}:
                continue
            text = extract_text(payload.get("content"))
            if not text or text.startswith("<turn_aborted>"):
                continue
            timestamp = str(event.get("timestamp") or "")
            phase = str(payload.get("phase") or "")
            messages.append((timestamp, role, phase, text))

    generated = datetime.now(timezone.utc).isoformat(timespec="seconds")
    lines = [
        "# User-visible Codex conversation transcript",
        "",
        f"- Thread ID: `{args.thread_id}`",
        f"- Source rollout: `{args.rollout}`",
        f"- Exported UTC: `{generated}`",
        f"- Messages: `{len(messages)}`",
        "- Scope: user and assistant messages visible in the conversation.",
        "- Excluded: system/developer instructions, hidden reasoning, raw tool calls/output, credentials, and interruption wrappers.",
        "",
    ]
    for index, (timestamp, role, phase, text) in enumerate(messages, start=1):
        phase_label = f", phase `{phase}`" if phase else ""
        lines.extend(
            [
                f"## {index}. {role.capitalize()} — `{timestamp}`{phase_label}",
                "",
                text,
                "",
            ]
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(messages)} messages to {args.output}")


if __name__ == "__main__":
    main()

