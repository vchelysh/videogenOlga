from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "SHA256SUMS.txt"
EXCLUDED_PARTS = {".git", ".idea", ".pytest_cache", "__pycache__"}
EXCLUDED_DIR_PREFIXES = (
    "source_frames_v5",
    "upscaled_frames",
    "v5_scene03_take01_",
)


def is_excluded(relative: Path) -> bool:
    return any(
        part in EXCLUDED_PARTS
        or any(part.startswith(prefix) for prefix in EXCLUDED_DIR_PREFIXES)
        for part in relative.parts
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    files = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or path == OUTPUT:
            continue
        relative = path.relative_to(ROOT)
        if is_excluded(relative):
            continue
        files.append((relative.as_posix(), path))
    lines = [f"{sha256(path)}  {relative}" for relative, path in sorted(files)]
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(lines)} checksums to {OUTPUT}")


if __name__ == "__main__":
    main()
