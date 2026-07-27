#!/usr/bin/env python3
"""Conservative local secret/artifact scanner for changed or repository files.

Findings require human/agent review; they are not proof of a credential.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable

EXCLUDED_DIRS = {
    ".git", "node_modules", "target", "build", "dist", ".gradle", ".venv",
    "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}
SUSPICIOUS_NAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "credentials.json", "service-account.json", "keystore.jks", "release.keystore",
}
SUSPICIOUS_SUFFIXES = {".pem", ".p12", ".pfx", ".jks", ".keystore", ".key", ".sql", ".dump"}
PATTERNS = [
    ("private-key", "high", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("openai-style-key", "high", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("github-token", "high", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", "high", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack-token", "high", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    (
        "generic-secret-assignment",
        "review",
        re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-/.+=]{16,}"),
    ),
]
TEXT_LIMIT = 2 * 1024 * 1024
LARGE_FILE_LIMIT = 50 * 1024 * 1024
ALLOW_FIXTURE_MARKER = "siyk-secret-scan: allow-test-fixture"
FIXTURE_DIRS = {"test", "tests", "fixture", "fixtures", "__fixtures__", "samples"}


def decode_status_paths(data: bytes) -> list[str]:
    fields = data.split(b"\0")
    result: list[str] = []
    i = 0
    while i < len(fields):
        field = fields[i]
        i += 1
        if not field:
            continue
        decoded = field.decode("utf-8", errors="replace")
        if len(decoded) < 3:
            continue
        code = decoded[:2]
        path = decoded[3:] if decoded[2:3] == " " else decoded[2:]
        result.append(path)
        if "R" in code or "C" in code:
            if i < len(fields) and fields[i]:
                i += 1
    return result


def git_changed_files(root: Path) -> list[Path]:
    cp = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "-uall"], cwd=root,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if cp.returncode != 0:
        return []
    result = []
    for raw in decode_status_paths(cp.stdout):
        path = (root / raw).resolve()
        try:
            path.relative_to(root.resolve())
        except ValueError:
            continue
        if path.is_file():
            result.append(path)
    return result


def all_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in EXCLUDED_DIRS for part in rel.parts):
            continue
        yield path


def fixture_marker_allowed(rel: Path, text: str) -> bool:
    first_lines = "\n".join(text.splitlines()[:10])
    return ALLOW_FIXTURE_MARKER in first_lines and any(part.lower() in FIXTURE_DIRS for part in rel.parts)


def scan(root: Path, changed_only: bool) -> dict:
    root = root.resolve()
    candidates = git_changed_files(root) if changed_only else list(all_files(root))
    unique_candidates = sorted(set(candidates))
    findings: list[dict] = []
    for path in unique_candidates:
        rel_path = path.relative_to(root)
        rel = rel_path.as_posix()
        if path.name in SUSPICIOUS_NAMES or path.suffix.lower() in SUSPICIOUS_SUFFIXES:
            findings.append({"file": rel, "kind": "suspicious-file", "severity": "review"})
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size > LARGE_FILE_LIMIT:
            findings.append({"file": rel, "kind": "large-file", "severity": "review", "size": size})
        if size > TEXT_LIMIT:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        marker_present = ALLOW_FIXTURE_MARKER in "\n".join(text.splitlines()[:10])
        if marker_present and fixture_marker_allowed(rel_path, text):
            continue
        if marker_present:
            findings.append({
                "file": rel,
                "kind": "invalid-fixture-allow-marker",
                "severity": "review",
                "line": next((i for i, line in enumerate(text.splitlines(), 1) if ALLOW_FIXTURE_MARKER in line), 1),
            })

        for kind, severity, pattern in PATTERNS:
            match = pattern.search(text)
            if match:
                findings.append({
                    "file": rel,
                    "kind": kind,
                    "severity": severity,
                    "line": text.count("\n", 0, match.start()) + 1,
                })
    return {
        "root": str(root),
        "mode": "git-changes" if changed_only else "repository",
        "files_scanned": len(unique_candidates),
        "findings": findings,
        "high_confidence_block": any(f["severity"] == "high" for f in findings),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Scan for likely secrets and generated artifacts")
    parser.add_argument("--root", default=".")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--git-changes", action="store_true", help="Scan changed and untracked files only")
    mode.add_argument("--all", action="store_true", help="Scan the whole repository")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    changed_only = not args.all
    result = scan(Path(args.root), changed_only)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 2 if result["high_confidence_block"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
