#!/usr/bin/env python3
"""Collect Git baseline and working-tree evidence without modifying the repository."""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

CONFLICT_CODES = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}


def run(root: Path, *args: str) -> tuple[int, bytes, bytes]:
    cp = subprocess.run(
        ["git", *args], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        check=False,
    )
    return cp.returncode, cp.stdout, cp.stderr


def text(data: bytes) -> str:
    return data.decode("utf-8", errors="replace").strip()


def parse_status_z(data: bytes) -> list[dict]:
    fields = data.split(b"\0")
    records: list[dict] = []
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
        record = {"status": code, "path": path}
        if "R" in code or "C" in code:
            if i < len(fields) and fields[i]:
                record["original_path"] = fields[i].decode("utf-8", errors="replace")
                i += 1
        records.append(record)
    return records


def parse_name_status_z(data: bytes) -> list[dict]:
    fields = data.split(b"\0")
    records: list[dict] = []
    i = 0
    while i < len(fields):
        status_raw = fields[i]
        i += 1
        if not status_raw:
            continue
        status = status_raw.decode("utf-8", errors="replace")
        if i >= len(fields):
            break
        path = fields[i].decode("utf-8", errors="replace")
        i += 1
        record = {"status": status, "path": path}
        if status.startswith(("R", "C")) and i < len(fields):
            record["new_path"] = fields[i].decode("utf-8", errors="replace")
            i += 1
        records.append(record)
    return records


def remote_map(repo: Path) -> dict[str, list[str]]:
    code, out, _ = run(repo, "remote", "-v")
    result: dict[str, list[str]] = {}
    if code != 0:
        return result
    for line in text(out).splitlines():
        parts = line.split()
        if len(parts) >= 2:
            result.setdefault(parts[0], [])
            if parts[1] not in result[parts[0]]:
                result[parts[0]].append(parts[1])
    return result


def remote_default_branch(repo: Path, remote: str = "origin") -> str | None:
    code, out, _ = run(repo, "symbolic-ref", "--quiet", "--short", f"refs/remotes/{remote}/HEAD")
    value = text(out)
    return value or None if code == 0 else None


def verify_commit(repo: Path, ref: str) -> str | None:
    code, out, _ = run(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    return text(out) or None if code == 0 else None


def collect(root: Path, base: str | None = None) -> dict:
    root = root.resolve()
    inside, top, err = run(root, "rev-parse", "--show-toplevel")
    if inside != 0:
        return {
            "root": str(root),
            "is_git_repository": False,
            "error": text(err) or "not a Git repository",
        }

    repo = Path(text(top)).resolve()
    _, branch_raw, _ = run(repo, "branch", "--show-current")
    branch = text(branch_raw) or None
    head = verify_commit(repo, "HEAD")
    _, upstream_raw, _ = run(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{upstream}")
    upstream = text(upstream_raw) or None
    status_code, status_raw, status_err = run(repo, "status", "--porcelain=v1", "-z", "-uall")
    status_records = parse_status_z(status_raw) if status_code == 0 else []

    selected_base = None
    base_source = None
    baseline_error = None
    if base:
        selected_base = verify_commit(repo, base)
        base_source = "explicit"
        if not selected_base:
            baseline_error = f"explicit baseline is not a commit: {base}"
    elif head and upstream:
        code, merge_base_raw, _ = run(repo, "merge-base", "HEAD", upstream)
        merge_base = text(merge_base_raw)
        if code == 0 and merge_base:
            selected_base, base_source = merge_base, "upstream-merge-base"
    if not selected_base and head:
        parent = verify_commit(repo, "HEAD^")
        if parent:
            selected_base, base_source = parent, "head-parent"

    committed_records: list[dict] = []
    diff_stat = ""
    if selected_base and head:
        code, out, _ = run(repo, "diff", "--name-status", "-z", f"{selected_base}...HEAD")
        if code == 0:
            committed_records = parse_name_status_z(out)
        code, stat_raw, _ = run(repo, "diff", "--stat", f"{selected_base}...HEAD")
        if code == 0:
            diff_stat = text(stat_raw)

    staged = [r for r in status_records if r["status"] not in {"??", "!!"} and r["status"][0] != " "]
    unstaged = [r for r in status_records if r["status"] not in {"??", "!!"} and len(r["status"]) > 1 and r["status"][1] != " "]
    untracked = [r for r in status_records if r["status"] == "??"]
    ignored = [r for r in status_records if r["status"] == "!!"]
    conflicted = [r for r in status_records if r["status"] in CONFLICT_CODES]

    changed_paths = set()
    for record in committed_records + status_records:
        for key in ("path", "new_path"):
            value = record.get(key)
            if value:
                changed_paths.add(value)

    ahead = behind = None
    if head and upstream:
        code, counts_raw, _ = run(repo, "rev-list", "--left-right", "--count", f"{upstream}...HEAD")
        counts = text(counts_raw).split()
        if code == 0 and len(counts) == 2:
            behind, ahead = int(counts[0]), int(counts[1])

    return {
        "root": str(repo),
        "is_git_repository": True,
        "branch": branch,
        "detached_head": bool(head and not branch),
        "head": head,
        "unborn_head": head is None,
        "upstream": upstream,
        "remote_default_branch": remote_default_branch(repo),
        "remotes": remote_map(repo),
        "ahead": ahead,
        "behind": behind,
        "baseline": selected_base,
        "baseline_source": base_source,
        "baseline_error": baseline_error,
        "status_error": text(status_err) if status_code != 0 else None,
        "status_records": status_records,
        "staged_changes": staged,
        "unstaged_changes": unstaged,
        "untracked_files": [r["path"] for r in untracked],
        "ignored_files": [r["path"] for r in ignored],
        "conflicted_files": [r["path"] for r in conflicted],
        "committed_changes": committed_records,
        "changed_files": sorted(changed_paths),
        "diff_stat": diff_stat,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect Git changes for siyk-test-new")
    parser.add_argument("--root", default=".")
    parser.add_argument("--base", default=None)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = collect(Path(args.root), args.base)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result.get("is_git_repository") else 1


if __name__ == "__main__":
    raise SystemExit(main())
