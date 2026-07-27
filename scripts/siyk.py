#!/usr/bin/env python3
"""Small deterministic helper CLI for siyrs-skill.

The agent owns business/test design. This CLI gathers evidence, validates state,
and normalizes command routing without mutating project source code.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from collect_git_changes import collect
from detect_project import detect
from fingerprint import fingerprint
from route_command import route
from scan_secrets import scan
from validate_bundle import validate


def main() -> int:
    parser = argparse.ArgumentParser(prog="siyk", description="siyrs-skill helper CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    p_route = sub.add_parser("route", help="Normalize a slash command or Chinese alias")
    p_route.add_argument("text")

    p_detect = sub.add_parser("detect", help="Detect repository project types")
    p_detect.add_argument("--root", default=".")

    p_changes = sub.add_parser("changes", help="Collect Git change evidence")
    p_changes.add_argument("--root", default=".")
    p_changes.add_argument("--base")

    p_fingerprint = sub.add_parser("fingerprint", help="Fingerprint repository/worktree state")
    p_fingerprint.add_argument("--root", default=".")

    p_scan = sub.add_parser("scan", help="Scan likely secrets/artifacts")
    p_scan.add_argument("--root", default=".")
    p_scan.add_argument("--all", action="store_true", help="Scan repository instead of Git changes")

    p_validate = sub.add_parser("validate", help="Validate this skill bundle")
    p_validate.add_argument("--root", default=".")

    args = parser.parse_args()
    if args.command == "route":
        result = route(args.text)
        code = 0 if result["matched"] else 1
    elif args.command == "detect":
        result = detect(Path(args.root))
        code = 0
    elif args.command == "changes":
        result = collect(Path(args.root), args.base)
        code = 0 if result.get("is_git_repository") else 1
    elif args.command == "fingerprint":
        result = fingerprint(Path(args.root))
        code = 0
    elif args.command == "scan":
        result = scan(Path(args.root), changed_only=not args.all)
        code = 2 if result["high_confidence_block"] else 0
    else:
        result = validate(Path(args.root))
        code = 0 if result["valid"] else 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
