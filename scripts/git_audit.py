#!/usr/bin/env python3
"""Deterministically audit Git Index or outgoing history without exposing secret values."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

TEXT_LIMIT = 2 * 1024 * 1024
DEFAULT_LARGE_LIMIT = 50 * 1024 * 1024
SUSPICIOUS_NAMES = {
    ".env", ".env.local", ".env.production", "id_rsa", "id_ed25519",
    "credentials.json", "service-account.json", "keystore.jks", "release.keystore",
}
SUSPICIOUS_SUFFIXES = {".pem", ".p12", ".pfx", ".jks", ".keystore", ".key", ".sql", ".dump"}
PATTERNS = [
    ("private-key", "high", "stop", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("openai-style-key", "high", "stop", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("github-token", "high", "stop", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("aws-access-key", "high", "stop", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("slack-token", "high", "stop", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
    (
        "generic-secret-assignment", "review", "review",
        re.compile(r"(?i)\b(?:api[_-]?key|secret|token|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-/.+=]{16,}"),
    ),
]


@dataclass(frozen=True)
class RawFinding:
    kind: str
    severity: str
    default_action: str
    path: str
    location: str
    classification: str
    evidence_fingerprint: str
    size: int | None = None
    commit: str | None = None


def run(repo: Path, *args: str, input_bytes: bytes | None = None) -> tuple[int, bytes, bytes]:
    completed = subprocess.run(
        ["git", *args], cwd=repo, input=input_bytes,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr


def git_text(repo: Path, *args: str) -> str:
    code, out, err = run(repo, *args)
    if code != 0:
        raise ValueError((err or out).decode("utf-8", errors="replace").strip() or f"git {' '.join(args)} failed")
    return out.decode("utf-8", errors="replace").strip()


def repository_root(root: Path) -> Path:
    return Path(git_text(root.resolve(), "rev-parse", "--show-toplevel")).resolve()


def fingerprint(kind: str, path: str, classification: str, value: str, location: str, commit: str | None = None) -> str:
    payload = "\0".join((kind, path, classification, location, commit or "", value)).encode("utf-8", errors="replace")
    return hashlib.sha256(payload).hexdigest()


def sensitive_path(path: str) -> bool:
    name = Path(path).name
    return name in SUSPICIOUS_NAMES or Path(path).suffix.casefold() in SUSPICIOUS_SUFFIXES or name.startswith(".env.")


def parse_name_status_z(data: bytes) -> list[dict[str, str]]:
    fields = data.split(b"\0")
    result: list[dict[str, str]] = []
    index = 0
    while index < len(fields):
        if not fields[index]:
            index += 1
            continue
        status = fields[index].decode("utf-8", errors="replace")
        index += 1
        if index >= len(fields):
            break
        old_path = fields[index].decode("utf-8", errors="replace")
        index += 1
        record = {"status": status, "path": old_path}
        if status.startswith(("R", "C")) and index < len(fields):
            record["path"] = fields[index].decode("utf-8", errors="replace")
            record["original_path"] = old_path
            index += 1
        result.append(record)
    return result


def match_text(text: str, *, path: str, classification: str, location_prefix: str, commit: str | None = None) -> list[RawFinding]:
    findings: list[RawFinding] = []
    for kind, severity, action, pattern in PATTERNS:
        for match in pattern.finditer(text):
            line = text.count("\n", 0, match.start()) + 1
            location = f"{location_prefix}:{line}"
            value = match.group(0)
            findings.append(RawFinding(
                kind=kind,
                severity=severity,
                default_action=action,
                path=path,
                location=location,
                classification=classification,
                evidence_fingerprint=fingerprint(kind, path, classification, value, location, commit),
                commit=commit,
            ))
    return findings


def patch_findings(patch: str, *, commit: str | None = None) -> list[RawFinding]:
    findings: list[RawFinding] = []
    current_path = "unknown"
    new_line = 0
    old_line = 0
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            current_path = "unknown"
            continue
        if line.startswith("+++ b/"):
            current_path = line[6:]
            continue
        if line.startswith("@@"):
            match = re.search(r"@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
            if match:
                old_line = int(match.group(1))
                new_line = int(match.group(2))
            continue
        if line.startswith("+") and not line.startswith("+++"):
            content = line[1:]
            findings.extend(match_text(
                content,
                path=current_path,
                classification="historical-introduction" if commit else "introduced",
                location_prefix=f"patch+{new_line}",
                commit=commit,
            ))
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            content = line[1:]
            findings.extend(match_text(
                content,
                path=current_path,
                classification="removed",
                location_prefix=f"patch-{old_line}",
                commit=commit,
            ))
            old_line += 1
        elif not line.startswith("\\"):
            old_line += 1
            new_line += 1
    return findings


def blob_bytes(repo: Path, spec: str) -> bytes:
    code, out, _ = run(repo, "show", spec)
    return out if code == 0 else b""


def blob_size(repo: Path, spec: str) -> int | None:
    code, out, _ = run(repo, "cat-file", "-s", spec)
    if code != 0:
        return None
    try:
        return int(out.strip())
    except ValueError:
        return None


def blob_findings(
    repo: Path,
    *,
    spec: str,
    path: str,
    classification: str,
    commit: str | None = None,
    large_limit: int = DEFAULT_LARGE_LIMIT,
) -> list[RawFinding]:
    findings: list[RawFinding] = []
    size = blob_size(repo, spec)
    if sensitive_path(path):
        findings.append(RawFinding(
            kind="suspicious-file",
            severity="review",
            default_action="review",
            path=path,
            location=spec,
            classification=classification,
            evidence_fingerprint=fingerprint("suspicious-file", path, classification, path, spec, commit),
            size=size,
            commit=commit,
        ))
    if size is not None and size > large_limit:
        findings.append(RawFinding(
            kind="large-blob",
            severity="review",
            default_action="review",
            path=path,
            location=spec,
            classification=classification,
            evidence_fingerprint=fingerprint("large-blob", path, classification, str(size), spec, commit),
            size=size,
            commit=commit,
        ))
    if size is None or size > TEXT_LIMIT:
        return findings
    data = blob_bytes(repo, spec)
    if b"\0" in data[:8192]:
        return findings
    text = data.decode("utf-8", errors="ignore")
    findings.extend(match_text(text, path=path, classification=classification, location_prefix=spec, commit=commit))
    return findings


def stable_findings(raw: Iterable[RawFinding]) -> list[dict]:
    unique: dict[tuple, RawFinding] = {}
    for finding in raw:
        key = (
            finding.kind, finding.path, finding.location, finding.classification,
            finding.evidence_fingerprint, finding.commit,
        )
        unique[key] = finding
    ordered = sorted(
        unique.values(),
        key=lambda item: (
            item.default_action != "stop", item.kind, item.path, item.commit or "", item.location,
            item.classification, item.evidence_fingerprint,
        ),
    )
    result: list[dict] = []
    for index, finding in enumerate(ordered, 1):
        item = asdict(finding)
        item["id"] = f"RISK-{index:03d}"
        result.append(item)
    return result


def audit_index(root: Path, *, large_limit: int = DEFAULT_LARGE_LIMIT) -> dict:
    repo = repository_root(root)
    code, names_raw, err = run(repo, "diff", "--cached", "--name-status", "-z")
    if code != 0:
        raise ValueError(err.decode("utf-8", errors="replace").strip() or "unable to inspect Git Index")
    changes = parse_name_status_z(names_raw)
    tree_oid = git_text(repo, "write-tree")
    code, patch_raw, err = run(repo, "diff", "--cached", "--no-ext-diff", "--no-color", "--unified=0")
    if code != 0:
        raise ValueError(err.decode("utf-8", errors="replace").strip() or "unable to inspect staged patch")
    raw_findings: list[RawFinding] = patch_findings(patch_raw.decode("utf-8", errors="replace"))
    paths: list[str] = []
    for change in changes:
        if change["status"].startswith("D"):
            continue
        path = change["path"]
        paths.append(path)
        raw_findings.extend(blob_findings(
            repo,
            spec=f":{path}",
            path=path,
            classification="present-in-index",
            large_limit=large_limit,
        ))
    findings = stable_findings(raw_findings)
    return {
        "root": str(repo),
        "phase": "index",
        "tree_oid": tree_oid,
        "paths": sorted(paths),
        "changes": changes,
        "findings": findings,
        "blocking_findings": [item["id"] for item in findings if item["default_action"] == "stop"],
        "high_confidence_block": any(item["default_action"] == "stop" for item in findings),
    }


def resolve_base(repo: Path, explicit: str | None) -> str:
    if explicit:
        return git_text(repo, "rev-parse", "--verify", f"{explicit}^{{commit}}")
    code, out, _ = run(repo, "rev-parse", "--verify", "@{upstream}^{commit}")
    if code == 0:
        return out.decode("ascii", errors="replace").strip()
    raise ValueError("outgoing audit requires --base when the current branch has no upstream")


def outgoing_object_findings(repo: Path, base: str, head: str, large_limit: int) -> list[RawFinding]:
    code, out, _ = run(repo, "rev-list", "--objects", f"{base}..{head}")
    if code != 0:
        return []
    lines = out.decode("utf-8", errors="replace").splitlines()
    queries = []
    path_by_oid: dict[str, str] = {}
    for line in lines:
        oid, _, path = line.partition(" ")
        if oid:
            queries.append(oid)
            if path:
                path_by_oid.setdefault(oid, path)
    if not queries:
        return []
    code, batch, _ = run(
        repo,
        "cat-file",
        "--batch-check=%(objectname) %(objecttype) %(objectsize)",
        input_bytes=("\n".join(queries) + "\n").encode("ascii"),
    )
    if code != 0:
        return []
    findings: list[RawFinding] = []
    for line in batch.decode("utf-8", errors="replace").splitlines():
        parts = line.split()
        if len(parts) != 3 or parts[1] != "blob":
            continue
        oid, _, size_text = parts
        try:
            size = int(size_text)
        except ValueError:
            continue
        if size <= large_limit:
            continue
        path = path_by_oid.get(oid, "<unknown>")
        findings.append(RawFinding(
            kind="large-outgoing-blob",
            severity="review",
            default_action="review",
            path=path,
            location=oid,
            classification="outgoing-object",
            evidence_fingerprint=fingerprint("large-outgoing-blob", path, "outgoing-object", str(size), oid),
            size=size,
        ))
    return findings


def audit_outgoing(root: Path, *, base: str | None = None, large_limit: int = DEFAULT_LARGE_LIMIT) -> dict:
    repo = repository_root(root)
    head = git_text(repo, "rev-parse", "--verify", "HEAD^{commit}")
    base_sha = resolve_base(repo, base)
    commits_text = git_text(repo, "rev-list", "--reverse", f"{base_sha}..{head}")
    commits = [item for item in commits_text.splitlines() if item]
    raw_findings: list[RawFinding] = []
    for commit in commits:
        code, patch_raw, _ = run(repo, "show", "--format=", "--no-ext-diff", "--no-color", "--unified=0", commit)
        if code == 0:
            raw_findings.extend(patch_findings(patch_raw.decode("utf-8", errors="replace"), commit=commit))

    code, tree_raw, _ = run(repo, "ls-tree", "-r", "-z", "--name-only", head)
    final_paths = [item.decode("utf-8", errors="replace") for item in tree_raw.split(b"\0") if item] if code == 0 else []
    for path in final_paths:
        raw_findings.extend(blob_findings(
            repo,
            spec=f"{head}:{path}",
            path=path,
            classification="present-in-final-head",
            commit=head,
            large_limit=large_limit,
        ))
    raw_findings.extend(outgoing_object_findings(repo, base_sha, head, large_limit))
    findings = stable_findings(raw_findings)
    return {
        "root": str(repo),
        "phase": "outgoing-history",
        "base": base_sha,
        "head": head,
        "commits": commits,
        "final_tree": git_text(repo, "rev-parse", f"{head}^{{tree}}"),
        "findings": findings,
        "blocking_findings": [item["id"] for item in findings if item["default_action"] == "stop"],
        "high_confidence_block": any(item["default_action"] == "stop" for item in findings),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit the exact Git content to be committed or pushed")
    parser.add_argument("--root", default=".")
    parser.add_argument("--phase", required=True, choices=["index", "outgoing"])
    parser.add_argument("--base")
    parser.add_argument("--large-limit", type=int, default=DEFAULT_LARGE_LIMIT)
    args = parser.parse_args()
    try:
        if args.phase == "index":
            result = audit_index(Path(args.root), large_limit=args.large_limit)
        else:
            result = audit_outgoing(Path(args.root), base=args.base, large_limit=args.large_limit)
    except (OSError, ValueError) as exc:
        result = {"error": str(exc), "phase": args.phase, "findings": [], "high_confidence_block": True}
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["high_confidence_block"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
