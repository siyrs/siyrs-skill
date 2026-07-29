#!/usr/bin/env python3
"""Resolve deterministic T1/T2/T3 execution plans from config schema v2."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from config_model import ConfigError, load_config

VALID_TIERS = {"t1", "t2", "t3"}
DEFAULT_TIMEOUT = 900


def _inside(root: Path, path: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _step(command: Any, *, root: Path, default_cwd: str, source: str, index: int) -> dict[str, Any]:
    if isinstance(command, str):
        return {
            "id": f"{source}:{index}",
            "source": source,
            "cwd": default_cwd,
            "command": command,
            "argv": None,
            "shell": True,
            "timeout_seconds": DEFAULT_TIMEOUT,
            "environment": {},
            "network": "inherit",
        }
    cwd = str(command.get("cwd") or default_cwd)
    resolved = (root / cwd).resolve()
    if not _inside(root, resolved):
        raise ConfigError(f"resolved command cwd escapes repository: {cwd}")
    command_text = command.get("command")
    argv = command.get("argv")
    return {
        "id": str(command.get("id") or f"{source}:{index}"),
        "source": source,
        "cwd": cwd,
        "command": command_text,
        "argv": list(argv) if isinstance(argv, list) else None,
        "shell": command_text is not None,
        "timeout_seconds": int(command.get("timeout_seconds", DEFAULT_TIMEOUT)),
        "environment": dict(command.get("environment") or {}),
        "network": command.get("network", "inherit"),
    }


def resolve_plan(root: Path, tier: str, modules: list[str] | None = None, config_path: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    tier = tier.casefold()
    if tier not in VALID_TIERS:
        raise ConfigError(f"unsupported tier: {tier}")
    loaded = load_config(root, config_path)
    if not loaded["valid"]:
        return {
            "valid": False,
            "tier": tier.upper(),
            "config_path": loaded["path"],
            "errors": loaded["errors"],
            "warnings": loaded["warnings"],
            "steps": [],
            "debts": ["configuration is invalid"],
        }
    config = loaded["config"]
    all_modules = config.get("project", {}).get("modules", [])
    by_name = {module["name"]: module for module in all_modules if isinstance(module, dict) and module.get("name")}
    requested = list(dict.fromkeys(modules or []))
    unknown = [name for name in requested if name not in by_name]
    if unknown:
        return {
            "valid": False,
            "tier": tier.upper(),
            "config_path": loaded["path"],
            "errors": [f"unknown module(s): {', '.join(unknown)}"],
            "warnings": loaded["warnings"],
            "steps": [],
            "debts": [],
        }
    selected = [by_name[name] for name in requested] if requested else list(all_modules)
    global_tier = config["testing"]["tiers"][tier]
    steps: list[dict[str, Any]] = []
    debts: list[str] = []
    warnings = list(loaded["warnings"])

    global_commands = global_tier.get("commands", [])
    for index, command in enumerate(global_commands):
        steps.append(_step(command, root=root, default_cwd=".", source=f"global:{tier}", index=index))

    for module in selected:
        name = module["name"]
        module_path = module["path"]
        module_tier = (((module.get("testing") or {}).get("tiers") or {}).get(tier) or {})
        commands = module_tier.get("commands", []) if isinstance(module_tier, dict) else []
        for index, command in enumerate(commands):
            steps.append(_step(command, root=root, default_cwd=module_path, source=f"module:{name}:{tier}", index=index))
        if not commands and not global_commands:
            debts.append(f"module {name} has no configured {tier.upper()} command")

    if not selected and not global_commands:
        debts.append(f"no configured {tier.upper()} commands")

    # Detect duplicate executable steps deterministically.
    signatures: set[tuple[Any, ...]] = set()
    deduped: list[dict[str, Any]] = []
    for step in steps:
        signature = (
            step["cwd"],
            step["command"],
            tuple(step["argv"] or []),
            tuple(sorted(step["environment"].items())),
        )
        if signature in signatures:
            warnings.append(f"duplicate plan step removed: {step['id']}")
            continue
        signatures.add(signature)
        deduped.append(step)
    steps = deduped

    selector_id = global_tier.get("selector_id") if tier == "t2" else None
    required_per_module = global_tier.get("required_per_module") if tier == "t2" else None
    require_real_uat = bool(global_tier.get("require_real_uat")) if tier == "t3" else None
    release_gate = bool(global_tier.get("release_gate")) if tier == "t3" else None

    if tier == "t2" and not selector_id:
        debts.append("T2 selector_id is missing")
    if tier == "t2" and not steps:
        debts.append("T2 has no machine-selectable execution command")
    if tier == "t3" and not steps:
        debts.append("T3 release gate has no configured execution command")

    return {
        "valid": bool(steps) and not any(debt.startswith("module ") for debt in debts),
        "tier": tier.upper(),
        "config_path": loaded["path"],
        "config_exists": loaded["exists"],
        "modules": [module["name"] for module in selected],
        "selector_id": selector_id,
        "required_per_module": required_per_module,
        "require_real_uat": require_real_uat,
        "release_gate": release_gate,
        "steps": steps,
        "debts": list(dict.fromkeys(debts)),
        "errors": [],
        "warnings": warnings,
        "environment": {"platform": os.name, "repository": str(root)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve a deterministic test-tier execution plan")
    parser.add_argument("--root", default=".")
    parser.add_argument("--config")
    parser.add_argument("--tier", required=True, choices=sorted(VALID_TIERS))
    parser.add_argument("--module", action="append", default=[])
    args = parser.parse_args()
    try:
        result = resolve_plan(
            Path(args.root), args.tier, args.module,
            Path(args.config) if args.config else None,
        )
    except (OSError, ConfigError) as exc:
        result = {"valid": False, "errors": [str(exc)], "steps": [], "debts": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
