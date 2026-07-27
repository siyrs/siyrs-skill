#!/usr/bin/env python3
"""Create a deterministic repository/worktree fingerprint for tested baselines."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Iterable

EXCLUDED = {
    ".git", "node_modules", "target", "build", "dist", "coverage", ".gradle",
    ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}
FULL_HASH_LIMIT = 10 * 1024 * 1024
PARTIAL_CHUNK = 64 * 1024


def run(root: Path, *args: str) -> tuple[int, bytes, bytes]:
    cp = subprocess.run(["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    return cp.returncode, cp.stdout, cp.stderr


def hash_file(hasher: "hashlib._Hash", root: Path, path: Path) -> None:
    try:
        rel_text = path.relative_to(root).as_posix()
    except ValueError:
        return
    hasher.update(b"PATH\0" + rel_text.encode("utf-8", errors="replace") + b"\0")
    try:
        size = path.stat().st_size
    except OSError:
        hasher.update(b"MISSING\0")
        return
    hasher.update(str(size).encode("ascii") + b"\0")
    try:
        with path.open("rb") as fh:
            if size <= FULL_HASH_LIMIT:
                while chunk := fh.read(1024 * 1024):
                    hasher.update(chunk)
            else:
                hasher.update(b"PARTIAL\0")
                hasher.update(fh.read(PARTIAL_CHUNK))
                fh.seek(max(0, size - PARTIAL_CHUNK))
                hasher.update(fh.read(PARTIAL_CHUNK))
    except OSError:
        hasher.update(b"UNREADABLE\0")


def iter_plain_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in EXCLUDED for part in rel.parts):
            continue
        yield path


def decode_nul_paths(data: bytes) -> list[str]:
    return [item.decode("utf-8", errors="replace") for item in data.split(b"\0") if item]


def fingerprint(root: Path) -> dict:
    root = root.resolve()
    hasher = hashlib.sha256()
    code, top, _ = run(root, "rev-parse", "--show-toplevel")
    if code == 0:
        repo = Path(top.decode("utf-8", errors="replace").strip()).resolve()
        code, head, _ = run(repo, "rev-parse", "--verify", "HEAD^{commit}")
        head_text = head.decode("ascii", errors="replace").strip() if code == 0 else "UNBORN"
        hasher.update(b"GIT\0" + head_text.encode("ascii", errors="replace") + b"\0")

        # Hash staged and unstaged patches independently so index-only changes are represented.
        _, staged_diff, _ = run(repo, "diff", "--binary", "--cached")
        _, unstaged_diff, _ = run(repo, "diff", "--binary")
        hasher.update(b"STAGED\0" + staged_diff)
        hasher.update(b"UNSTAGED\0" + unstaged_diff)

        _, untracked_raw, _ = run(repo, "ls-files", "--others", "--exclude-standard", "-z")
        untracked = sorted(decode_nul_paths(untracked_raw))
        for rel in untracked:
            hash_file(hasher, repo, repo / rel)

        _, submodule_raw, _ = run(repo, "submodule", "status", "--recursive")
        hasher.update(b"SUBMODULES\0" + submodule_raw)
        return {
            "root": str(repo),
            "mode": "git-worktree",
            "head": head_text,
            "untracked_files": len(untracked),
            "sha256": hasher.hexdigest(),
        }

    hasher.update(b"PLAIN\0")
    files = sorted(iter_plain_files(root))
    for path in files:
        hash_file(hasher, root, path)
    return {"root": str(root), "mode": "plain-directory", "files": len(files), "sha256": hasher.hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Fingerprint a repository or directory")
    parser.add_argument("--root", default=".")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    print(json.dumps(fingerprint(Path(args.root)), ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
