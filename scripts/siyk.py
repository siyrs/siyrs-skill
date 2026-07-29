#!/usr/bin/env python3
"""Unified deterministic helper CLI for siyrs-skill."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from collect_git_changes import collect
from command_registry import registry_document
from config_model import ConfigError, load_config
from detect_project import detect
from fingerprint import fingerprint
from git_audit import audit_index, audit_outgoing
from route_command import route
from scan_secrets import scan
from test_plan import resolve_plan
from validate_bundle import validate


def main() -> int:
    parser = argparse.ArgumentParser(prog="siyk", description="siyrs-skill deterministic helpers")
    sub = parser.add_subparsers(dest="command", required=True)

    route_parser = sub.add_parser("route")
    route_parser.add_argument("text")
    route_parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))

    registry_parser = sub.add_parser("registry")
    registry_parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))

    detect_parser = sub.add_parser("detect")
    detect_parser.add_argument("--root", default=".")

    changes_parser = sub.add_parser("changes")
    changes_parser.add_argument("--root", default=".")
    changes_parser.add_argument("--base")
    changes_parser.add_argument("--purpose", choices=["t1", "add", "generic"], default="t1")

    fingerprint_parser = sub.add_parser("fingerprint")
    fingerprint_parser.add_argument("--root", default=".")

    scan_parser = sub.add_parser("scan")
    scan_parser.add_argument("--root", default=".")
    scan_parser.add_argument("--all", action="store_true")

    config_parser = sub.add_parser("config")
    config_parser.add_argument("action", choices=["validate"])
    config_parser.add_argument("--root", default=".")
    config_parser.add_argument("--file")
    config_parser.add_argument("--required", action="store_true")

    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("--root", default=".")
    plan_parser.add_argument("--config")
    plan_parser.add_argument("--tier", choices=["t1", "t2", "t3"], required=True)
    plan_parser.add_argument("--module", action="append", default=[])

    audit_parser = sub.add_parser("audit")
    audit_parser.add_argument("--root", default=".")
    audit_parser.add_argument("--phase", choices=["index", "outgoing"], required=True)
    audit_parser.add_argument("--base")
    audit_parser.add_argument("--large-limit", type=int, default=50 * 1024 * 1024)

    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--root", default=".")

    args = parser.parse_args()
    try:
        if args.command == "route":
            result = route(args.text, Path(args.root))
            code = 0 if result["matched"] and result["valid"] else (2 if result["matched"] else 1)
        elif args.command == "registry":
            result = registry_document(Path(args.root))
            code = 0
        elif args.command == "detect":
            result = detect(Path(args.root))
            code = 0
        elif args.command == "changes":
            result = collect(Path(args.root), args.base, args.purpose)
            code = 0 if result.get("is_git_repository") else 1
        elif args.command == "fingerprint":
            result = fingerprint(Path(args.root))
            code = 0
        elif args.command == "scan":
            result = scan(Path(args.root), changed_only=not args.all)
            code = 2 if result["high_confidence_block"] else 0
        elif args.command == "config":
            result = load_config(
                Path(args.root), Path(args.file) if args.file else None,
                required=args.required,
            )
            code = 0 if result["valid"] else 1
        elif args.command == "plan":
            result = resolve_plan(
                Path(args.root), args.tier, args.module,
                Path(args.config) if args.config else None,
            )
            code = 0 if result["valid"] else 1
        elif args.command == "audit":
            if args.phase == "index":
                result = audit_index(Path(args.root), large_limit=args.large_limit)
            else:
                result = audit_outgoing(Path(args.root), base=args.base, large_limit=args.large_limit)
            code = 2 if result["high_confidence_block"] else 0
        else:
            result = validate(Path(args.root))
            code = 0 if result["valid"] else 1
    except (OSError, ValueError, ConfigError, json.JSONDecodeError) as exc:
        result = {"error": str(exc)}
        code = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
