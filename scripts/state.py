#!/usr/bin/env python3
"""Read, migrate, atomically update, and promote .siyrs/state.json schema v2."""
from __future__ import annotations

import argparse
import json
import os
import subprocess
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

STATE_VERSION = 2
STATUSES = {"complete", "partially-complete", "failed", "blocked", "unknown"}
KINDS = {"authoring", "t1", "t2", "t3"}
RELEASE_DECISIONS = {"passed", "failed", "blocked", "unknown", "provisional"}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def empty_record(kind: str) -> dict[str, Any]:
    record: dict[str, Any] = {
        "kind": kind,
        "commit": None,
        "fingerprint": None,
        "tree_oid": None,
        "baseline_commit": None,
        "status": None,
        "results_file": None,
        "case_ids": [],
        "modules": [],
        "expanded_modules": [],
        "blocked_suites": [],
        "updated_at": None,
    }
    if kind == "authoring":
        record["depth"] = None
    if kind == "t1":
        record["promotion"] = None
    if kind == "t2":
        record["selector_id"] = None
    if kind == "t3":
        record["release_gate"] = None
        record["coverage"] = None
    return record


def default_state() -> dict[str, Any]:
    return {
        "version": STATE_VERSION,
        "last_authoring": empty_record("authoring"),
        "last_t1_run": empty_record("t1"),
        "last_t2_run": empty_record("t2"),
        "last_t3_run": empty_record("t3"),
        "last_release_gate": None,
        "migration": None,
        "updated_at": None,
    }


def migrate_v1(data: dict[str, Any]) -> dict[str, Any]:
    migrated = default_state()
    incremental_commit = data.get("last_incremental_test_commit")
    incremental_fp = data.get("last_incremental_test_fingerprint")
    if incremental_commit or incremental_fp:
        migrated["last_authoring"].update({
            "commit": incremental_commit,
            "fingerprint": incremental_fp,
            "depth": data.get("last_incremental_test_mode"),
            "status": "unknown",
            "results_file": data.get("last_results_file"),
            "updated_at": data.get("updated_at"),
        })
    full_commit = data.get("last_full_test_commit")
    full_fp = data.get("last_full_test_fingerprint")
    if full_commit or full_fp:
        migrated["last_t3_run"].update({
            "commit": full_commit,
            "fingerprint": full_fp,
            "status": "unknown",
            "results_file": data.get("last_results_file"),
            "release_gate": "unknown",
            "updated_at": data.get("updated_at"),
        })
        migrated["last_release_gate"] = {
            "decision": "unknown",
            "commit": full_commit,
            "fingerprint": full_fp,
            "results_file": data.get("last_results_file"),
            "updated_at": data.get("updated_at"),
        }
    migrated_at = now_iso()
    migrated["migration"] = {
        "from_version": 1,
        "migrated_at": migrated_at,
        "note": "Legacy full/incremental evidence preserved with unknown completion semantics.",
    }
    migrated["updated_at"] = data.get("updated_at") or migrated_at
    return migrated


def normalize_v2(data: dict[str, Any]) -> dict[str, Any]:
    result = default_state()
    result.update(data)
    for key, kind in (
        ("last_authoring", "authoring"),
        ("last_t1_run", "t1"),
        ("last_t2_run", "t2"),
        ("last_t3_run", "t3"),
    ):
        record = empty_record(kind)
        existing = result.get(key)
        if isinstance(existing, dict):
            record.update(existing)
        record["kind"] = kind
        result[key] = record
    result["version"] = STATE_VERSION
    return result


def load(path: Path, *, auto_migrate: bool = True) -> dict[str, Any]:
    if not path.exists():
        return default_state()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state file must contain a JSON object")
    version = data.get("version", 1)
    if version == 1:
        if not auto_migrate:
            raise ValueError("state v1 requires migration")
        return migrate_v1(data)
    if version != STATE_VERSION:
        raise ValueError(f"unsupported state version: {version}")
    return normalize_v2(data)


def save(path: Path, data: dict[str, Any]) -> None:
    if data.get("version") != STATE_VERSION:
        raise ValueError(f"state version must be {STATE_VERSION}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tmp.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    tmp.replace(path)


def _unique(values: list[str] | None) -> list[str]:
    return list(dict.fromkeys(values or []))


def update_state(
    data: dict[str, Any],
    *,
    kind: str,
    status: str,
    commit: str | None = None,
    fingerprint: str | None = None,
    tree_oid: str | None = None,
    baseline_commit: str | None = None,
    results_file: str | None = None,
    depth: str | None = None,
    selector_id: str | None = None,
    release_gate: str | None = None,
    coverage: float | None = None,
    case_ids: list[str] | None = None,
    modules: list[str] | None = None,
    expanded_modules: list[str] | None = None,
    blocked_suites: list[str] | None = None,
) -> dict[str, Any]:
    if kind not in KINDS:
        raise ValueError(f"unsupported state kind: {kind}")
    if status not in STATUSES:
        raise ValueError(f"unsupported status: {status}")
    if not commit and not fingerprint:
        raise ValueError("state update requires a commit or fingerprint")
    if kind == "authoring" and depth not in {"quick", "standard", "strict"}:
        raise ValueError("authoring update requires depth quick|standard|strict")
    if kind == "t2" and not selector_id:
        raise ValueError("T2 update requires selector_id")
    if kind == "t3" and release_gate not in RELEASE_DECISIONS:
        raise ValueError("T3 update requires a valid release_gate decision")
    if kind != "t1" and tree_oid is not None:
        raise ValueError("tree_oid is currently supported only for T1 records")
    if coverage is not None and not 0 <= coverage <= 100:
        raise ValueError("coverage must be between 0 and 100")
    if kind == "t3" and release_gate == "passed" and not commit:
        raise ValueError("T3 release_gate=passed requires a durable commit; use provisional for a worktree fingerprint")

    updated = normalize_v2(deepcopy(data))
    key = {
        "authoring": "last_authoring",
        "t1": "last_t1_run",
        "t2": "last_t2_run",
        "t3": "last_t3_run",
    }[kind]
    timestamp = now_iso()
    record = empty_record(kind)
    record.update({
        "commit": commit,
        "fingerprint": fingerprint,
        "tree_oid": tree_oid,
        "baseline_commit": baseline_commit,
        "status": status,
        "results_file": results_file,
        "case_ids": _unique(case_ids),
        "modules": _unique(modules),
        "expanded_modules": _unique(expanded_modules),
        "blocked_suites": _unique(blocked_suites),
        "updated_at": timestamp,
    })
    if kind == "authoring":
        record["depth"] = depth
    elif kind == "t2":
        record["selector_id"] = selector_id
    elif kind == "t3":
        record["release_gate"] = release_gate
        record["coverage"] = coverage
        updated["last_release_gate"] = {
            "decision": release_gate,
            "commit": commit,
            "fingerprint": fingerprint,
            "results_file": results_file,
            "updated_at": timestamp,
        }
    updated[key] = record
    updated["updated_at"] = timestamp
    return updated


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, check=False,
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or f"git {' '.join(args)} failed"
        raise ValueError(message)
    return completed.stdout.strip()


def promote_t1(
    root: Path,
    data: dict[str, Any],
    *,
    commit: str = "HEAD",
    expected_fingerprint: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    record = normalize_v2(data)["last_t1_run"]
    if record.get("status") != "complete":
        raise ValueError("only a complete T1 result can be promoted to a commit")
    fingerprint = record.get("fingerprint")
    if not fingerprint:
        raise ValueError("T1 promotion requires a pre-commit fingerprint")
    if expected_fingerprint and fingerprint != expected_fingerprint:
        raise ValueError("T1 fingerprint does not match --expected-fingerprint")
    expected_tree = record.get("tree_oid")
    if not expected_tree:
        raise ValueError("T1 promotion requires tree_oid captured from the staged candidate tree")

    commit_sha = _git(root, "rev-parse", "--verify", f"{commit}^{{commit}}")
    commit_tree = _git(root, "rev-parse", "--verify", f"{commit_sha}^{{tree}}")
    if commit_tree != expected_tree:
        raise ValueError(
            f"commit tree {commit_tree} does not match tested candidate tree {expected_tree}; rerun T1 after restaging"
        )

    updated = normalize_v2(deepcopy(data))
    promoted_at = now_iso()
    promoted = dict(updated["last_t1_run"])
    promoted["commit"] = commit_sha
    promoted["tree_oid"] = commit_tree
    promoted["promotion"] = {
        "from_fingerprint": fingerprint,
        "commit": commit_sha,
        "tree_oid": commit_tree,
        "promoted_at": promoted_at,
    }
    promoted["updated_at"] = promoted_at
    updated["last_t1_run"] = promoted
    updated["updated_at"] = promoted_at
    return updated


def _csv(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage .siyrs/state.json schema v2")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show")
    sub.add_parser("migrate")

    update = sub.add_parser("update")
    update.add_argument("--kind", choices=sorted(KINDS), required=True)
    update.add_argument("--status", choices=sorted(STATUSES), required=True)
    update.add_argument("--commit")
    update.add_argument("--fingerprint")
    update.add_argument("--tree-oid")
    update.add_argument("--baseline-commit")
    update.add_argument("--results-file")
    update.add_argument("--depth", choices=["quick", "standard", "strict"])
    update.add_argument("--selector-id")
    update.add_argument("--release-gate", choices=sorted(RELEASE_DECISIONS))
    update.add_argument("--coverage", type=float)
    update.add_argument("--case-ids")
    update.add_argument("--modules")
    update.add_argument("--expanded-modules")
    update.add_argument("--blocked-suites")

    promote = sub.add_parser("promote-t1")
    promote.add_argument("--commit", default="HEAD")
    promote.add_argument("--expected-fingerprint")

    args = parser.parse_args()
    root = Path(args.root).resolve()
    path = root / ".siyrs" / "state.json"
    try:
        data = load(path)
        if args.command == "show":
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        if args.command == "migrate":
            save(path, data)
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        if args.command == "promote-t1":
            data = promote_t1(root, data, commit=args.commit, expected_fingerprint=args.expected_fingerprint)
        else:
            data = update_state(
                data,
                kind=args.kind,
                status=args.status,
                commit=args.commit,
                fingerprint=args.fingerprint,
                tree_oid=args.tree_oid,
                baseline_commit=args.baseline_commit,
                results_file=args.results_file,
                depth=args.depth,
                selector_id=args.selector_id,
                release_gate=args.release_gate,
                coverage=args.coverage,
                case_ids=_csv(args.case_ids),
                modules=_csv(args.modules),
                expanded_modules=_csv(args.expanded_modules),
                blocked_suites=_csv(args.blocked_suites),
            )
        save(path, data)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
