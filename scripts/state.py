#!/usr/bin/env python3
"""Read or safely update .siyrs/state.json."""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

STATE_VERSION = 1
DEFAULT = {
    "version": STATE_VERSION,
    "last_full_test_commit": None,
    "last_full_test_fingerprint": None,
    "last_full_test_mode": None,
    "last_incremental_test_commit": None,
    "last_incremental_test_fingerprint": None,
    "last_incremental_test_mode": None,
    "last_results_file": None,
    "updated_at": None,
}


def load(path: Path) -> dict:
    if not path.exists():
        return dict(DEFAULT)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("state file must contain a JSON object")
    version = data.get("version", STATE_VERSION)
    if version != STATE_VERSION:
        raise ValueError(f"unsupported state version: {version}")
    merged = dict(DEFAULT)
    merged.update(data)
    return merged


def save(path: Path, data: dict) -> None:
    if data.get("version") != STATE_VERSION:
        raise ValueError(f"state version must be {STATE_VERSION}")
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    with tmp.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(payload)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(path)


def update_state(
    data: dict,
    *,
    kind: str,
    mode: str,
    commit: str | None = None,
    fingerprint: str | None = None,
    results_file: str | None = None,
) -> dict:
    if kind not in {"full", "incremental"}:
        raise ValueError(f"unsupported state kind: {kind}")
    if mode not in {"quick", "standard", "strict"}:
        raise ValueError(f"unsupported test mode: {mode}")
    if not commit and not fingerprint:
        raise ValueError("state update requires a commit or fingerprint")
    updated = dict(DEFAULT)
    updated.update(data)
    prefix = "last_full_test" if kind == "full" else "last_incremental_test"
    updated[f"{prefix}_commit"] = commit
    updated[f"{prefix}_fingerprint"] = fingerprint
    updated[f"{prefix}_mode"] = mode
    if results_file is not None:
        updated["last_results_file"] = results_file
    updated["updated_at"] = datetime.now(timezone.utc).isoformat()
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage .siyrs/state.json")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("show")
    update = sub.add_parser("update")
    update.add_argument("--kind", choices=["full", "incremental"], required=True)
    update.add_argument("--commit")
    update.add_argument("--fingerprint")
    update.add_argument("--mode", choices=["quick", "standard", "strict"], required=True)
    update.add_argument("--results-file")
    args = parser.parse_args()

    path = Path(args.root).resolve() / ".siyrs" / "state.json"
    try:
        data = load(path)
        if args.command == "show":
            print(json.dumps(data, ensure_ascii=False, indent=2))
            return 0
        data = update_state(
            data,
            kind=args.kind,
            mode=args.mode,
            commit=args.commit,
            fingerprint=args.fingerprint,
            results_file=args.results_file,
        )
        save(path, data)
    except (ValueError, json.JSONDecodeError, OSError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
