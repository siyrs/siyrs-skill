#!/usr/bin/env python3
"""Parse, validate, and normalize .siyrs/config.yaml using the standard library.

The parser intentionally supports the conservative YAML subset used by siyrs-skill:
space-indented mappings/lists, quoted or plain scalars, inline JSON arrays/objects,
booleans, nulls, and numbers. Unsupported YAML features fail closed.
"""
from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CONFIG_VERSION = 2
VALID_DEPTHS = {"quick", "standard", "strict"}
VALID_INTEGRATIONS = {"rebase", "merge", "ff-only"}
VALID_PREFLIGHT = {
    "commit": {"t1", "none"},
    "sync_after_integration": {"t1", "none"},
    "pr": {"t2", "none"},
}

DEFAULT_CONFIG: dict[str, Any] = {
    "version": CONFIG_VERSION,
    "project": {"name": "auto", "type": "auto", "modules": []},
    "git": {
        "default_branch": "auto",
        "remote": "origin",
        "sync_mode": "current-branch",
        "integration": "rebase",
        "create_pr": False,
    },
    "testing": {
        "authoring": {"default_depth": "standard"},
        "tiers": {
            "t1": {"commands": [], "baseline": "last-t1-or-t3"},
            "t2": {
                "selector_id": "smoke-v1",
                "commands": [],
                "required_per_module": {"main_path": 1, "boundary": 1},
            },
            "t3": {"commands": [], "require_real_uat": True, "release_gate": True},
        },
        "preflight": {"commit": "t1", "sync_after_integration": "t1", "pr": "t2"},
        "coverage": {"enabled": True, "minimum": 80},
    },
    "paths": {"docs": "docs", "reports": "reports/testing"},
    "exclude": [
        ".git", ".idea", ".vscode", "node_modules", "target", "build", "dist",
        "coverage", ".gradle", ".pytest_cache", "__pycache__", "source",
    ],
}


@dataclass(frozen=True)
class ParsedLine:
    indent: int
    content: str
    lineno: int


class ConfigError(ValueError):
    """Raised for deterministic configuration parsing/validation failures."""


def _strip_comment(line: str) -> str:
    quote: str | None = None
    escaped = False
    for index, char in enumerate(line):
        if escaped:
            escaped = False
            continue
        if char == "\\" and quote == '"':
            escaped = True
            continue
        if quote:
            if char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            quote = char
            continue
        if char == "#" and (index == 0 or line[index - 1].isspace()):
            return line[:index].rstrip()
    return line.rstrip()


def _scalar(raw: str, lineno: int) -> Any:
    raw = raw.strip()
    if raw == "":
        return None
    lowered = raw.casefold()
    if lowered in {"null", "none", "~"}:
        return None
    if lowered in {"true", "false"}:
        return lowered == "true"
    if raw.startswith(("[", "{", '"')):
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ConfigError(f"invalid inline JSON at line {lineno}: {exc.msg}") from exc
    if raw.startswith("'"):
        if not raw.endswith("'") or len(raw) < 2:
            raise ConfigError(f"unterminated single-quoted scalar at line {lineno}")
        return raw[1:-1].replace("''", "'")
    if re.fullmatch(r"[-+]?\d+", raw):
        return int(raw)
    if re.fullmatch(r"[-+]?(?:\d+\.\d*|\d*\.\d+)(?:[eE][-+]?\d+)?", raw):
        return float(raw)
    return raw


def _tokenize(text: str) -> list[ParsedLine]:
    lines: list[ParsedLine] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        if "\t" in raw[: len(raw) - len(raw.lstrip(" \t"))]:
            raise ConfigError(f"tabs are not supported for indentation at line {lineno}")
        cleaned = _strip_comment(raw)
        if not cleaned.strip():
            continue
        indent = len(cleaned) - len(cleaned.lstrip(" "))
        if indent % 2:
            raise ConfigError(f"indentation must use multiples of two spaces at line {lineno}")
        lines.append(ParsedLine(indent, cleaned.strip(), lineno))
    return lines


def parse_yaml_subset(text: str) -> Any:
    lines = _tokenize(text)
    if not lines:
        return {}
    index, value = _parse_block(lines, 0, lines[0].indent)
    if index != len(lines):
        line = lines[index]
        raise ConfigError(f"unexpected content at line {line.lineno}")
    return value


def _parse_block(lines: list[ParsedLine], index: int, indent: int) -> tuple[int, Any]:
    if index >= len(lines) or lines[index].indent != indent:
        raise ConfigError("internal parser indentation mismatch")
    if lines[index].content.startswith("-"):
        return _parse_list(lines, index, indent)
    return _parse_mapping(lines, index, indent)


def _split_key_value(content: str, lineno: int) -> tuple[str, str]:
    if ":" not in content:
        raise ConfigError(f"expected key: value at line {lineno}")
    key, raw = content.split(":", 1)
    key = key.strip()
    if not key or not re.fullmatch(r"[A-Za-z0-9_.-]+", key):
        raise ConfigError(f"invalid mapping key {key!r} at line {lineno}")
    return key, raw.strip()


def _parse_mapping(lines: list[ParsedLine], index: int, indent: int) -> tuple[int, dict[str, Any]]:
    result: dict[str, Any] = {}
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ConfigError(f"unexpected indentation at line {line.lineno}")
        if line.content.startswith("-"):
            break
        key, raw = _split_key_value(line.content, line.lineno)
        if key in result:
            raise ConfigError(f"duplicate key {key!r} at line {line.lineno}")
        index += 1
        if raw:
            result[key] = _scalar(raw, line.lineno)
        elif index < len(lines) and lines[index].indent > indent:
            child_indent = lines[index].indent
            if child_indent != indent + 2:
                raise ConfigError(f"nested indentation must increase by two spaces at line {lines[index].lineno}")
            index, result[key] = _parse_block(lines, index, child_indent)
        else:
            result[key] = {}
    return index, result


def _parse_list(lines: list[ParsedLine], index: int, indent: int) -> tuple[int, list[Any]]:
    result: list[Any] = []
    while index < len(lines):
        line = lines[index]
        if line.indent < indent:
            break
        if line.indent > indent:
            raise ConfigError(f"unexpected indentation at line {line.lineno}")
        if not line.content.startswith("-"):
            break
        payload = line.content[1:].strip()
        index += 1
        if not payload:
            if index >= len(lines) or lines[index].indent != indent + 2:
                raise ConfigError(f"list item requires nested content at line {line.lineno}")
            index, value = _parse_block(lines, index, indent + 2)
            result.append(value)
            continue
        if ":" not in payload:
            result.append(_scalar(payload, line.lineno))
            continue

        item: dict[str, Any] = {}
        key, raw = _split_key_value(payload, line.lineno)
        if raw:
            item[key] = _scalar(raw, line.lineno)
        elif index < len(lines) and lines[index].indent > indent:
            if lines[index].indent != indent + 4:
                raise ConfigError(f"nested list mapping indentation is invalid at line {lines[index].lineno}")
            index, item[key] = _parse_block(lines, index, indent + 4)
        else:
            item[key] = {}

        while index < len(lines) and lines[index].indent == indent + 2 and not lines[index].content.startswith("-"):
            child = lines[index]
            child_key, child_raw = _split_key_value(child.content, child.lineno)
            if child_key in item:
                raise ConfigError(f"duplicate key {child_key!r} at line {child.lineno}")
            index += 1
            if child_raw:
                item[child_key] = _scalar(child_raw, child.lineno)
            elif index < len(lines) and lines[index].indent > indent + 2:
                if lines[index].indent != indent + 4:
                    raise ConfigError(f"nested list mapping indentation is invalid at line {lines[index].lineno}")
                index, item[child_key] = _parse_block(lines, index, indent + 4)
            else:
                item[child_key] = {}
        result.append(item)
    return index, result


def _merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    result = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _is_safe_relative_path(value: str) -> bool:
    path = Path(value)
    return bool(value) and not path.is_absolute() and ".." not in path.parts


def _validate_command(value: Any, location: str, errors: list[str]) -> None:
    if isinstance(value, str):
        if not value.strip():
            errors.append(f"{location} must not be empty")
        return
    if not isinstance(value, dict):
        errors.append(f"{location} must be a string or object")
        return
    command = value.get("command")
    argv = value.get("argv")
    if (command is None) == (argv is None):
        errors.append(f"{location} must define exactly one of command or argv")
    if command is not None and (not isinstance(command, str) or not command.strip()):
        errors.append(f"{location}.command must be a non-empty string")
    if argv is not None and (not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv)):
        errors.append(f"{location}.argv must be a non-empty string array")
    if "cwd" in value and (not isinstance(value["cwd"], str) or not _is_safe_relative_path(value["cwd"])):
        errors.append(f"{location}.cwd must be a safe relative path")
    if "timeout_seconds" in value and (not isinstance(value["timeout_seconds"], int) or value["timeout_seconds"] <= 0):
        errors.append(f"{location}.timeout_seconds must be a positive integer")
    if "environment" in value:
        env = value["environment"]
        if not isinstance(env, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in env.items()):
            errors.append(f"{location}.environment must be a string map")
    if "network" in value and value["network"] not in {"allow", "deny", "inherit"}:
        errors.append(f"{location}.network must be allow|deny|inherit")


def validate_config(data: Any, root: Path | None = None) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return {"valid": False, "errors": ["configuration root must be an object"], "warnings": []}
    if data.get("version") != CONFIG_VERSION:
        errors.append(f"version must be {CONFIG_VERSION}")

    project = data.get("project", {})
    modules = project.get("modules", []) if isinstance(project, dict) else []
    if not isinstance(modules, list):
        errors.append("project.modules must be an array")
        modules = []
    names: set[str] = set()
    paths: set[str] = set()
    for index, module in enumerate(modules):
        location = f"project.modules[{index}]"
        if not isinstance(module, dict):
            errors.append(f"{location} must be an object")
            continue
        name, path = module.get("name"), module.get("path")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"{location}.name must be a non-empty string")
        elif name in names:
            errors.append(f"duplicate module name: {name}")
        else:
            names.add(name)
        if not isinstance(path, str) or not _is_safe_relative_path(path):
            errors.append(f"{location}.path must be a safe relative path")
        elif path in paths:
            errors.append(f"duplicate module path: {path}")
        else:
            paths.add(path)
            if root is not None and not (root / path).exists():
                warnings.append(f"module path does not exist yet: {path}")
        module_testing = module.get("testing")
        if module_testing is not None and not isinstance(module_testing, dict):
            errors.append(f"{location}.testing must be an object")

    git = data.get("git", {})
    if not isinstance(git, dict):
        errors.append("git must be an object")
    else:
        if git.get("sync_mode", "current-branch") != "current-branch":
            errors.append("git.sync_mode must be current-branch")
        if git.get("integration", "rebase") not in VALID_INTEGRATIONS:
            errors.append("git.integration must be rebase|merge|ff-only")

    testing = data.get("testing", {})
    if not isinstance(testing, dict):
        errors.append("testing must be an object")
        testing = {}
    authoring = testing.get("authoring", {})
    if not isinstance(authoring, dict) or authoring.get("default_depth", "standard") not in VALID_DEPTHS:
        errors.append("testing.authoring.default_depth must be quick|standard|strict")

    tiers = testing.get("tiers", {})
    if not isinstance(tiers, dict):
        errors.append("testing.tiers must be an object")
        tiers = {}
    for tier in ("t1", "t2", "t3"):
        value = tiers.get(tier, {})
        if not isinstance(value, dict):
            errors.append(f"testing.tiers.{tier} must be an object")
            continue
        commands = value.get("commands", [])
        if not isinstance(commands, list):
            errors.append(f"testing.tiers.{tier}.commands must be an array")
        else:
            for index, command in enumerate(commands):
                _validate_command(command, f"testing.tiers.{tier}.commands[{index}]", errors)
    t2 = tiers.get("t2", {}) if isinstance(tiers.get("t2", {}), dict) else {}
    if not isinstance(t2.get("selector_id", ""), str) or not t2.get("selector_id", "").strip():
        errors.append("testing.tiers.t2.selector_id must be a non-empty string")
    required = t2.get("required_per_module", {})
    if not isinstance(required, dict):
        errors.append("testing.tiers.t2.required_per_module must be an object")
    else:
        for key in ("main_path", "boundary"):
            if not isinstance(required.get(key), int) or required.get(key, 0) < 1:
                errors.append(f"testing.tiers.t2.required_per_module.{key} must be >= 1")

    preflight = testing.get("preflight", {})
    if not isinstance(preflight, dict):
        errors.append("testing.preflight must be an object")
    else:
        for key, allowed in VALID_PREFLIGHT.items():
            if preflight.get(key, DEFAULT_CONFIG["testing"]["preflight"][key]) not in allowed:
                errors.append(f"testing.preflight.{key} must be one of {sorted(allowed)}")

    # Validate module command overrides with the same contract.
    for index, module in enumerate(modules):
        if not isinstance(module, dict):
            continue
        module_tiers = (((module.get("testing") or {}).get("tiers") or {}) if isinstance(module.get("testing") or {}, dict) else {})
        if not isinstance(module_tiers, dict):
            errors.append(f"project.modules[{index}].testing.tiers must be an object")
            continue
        for tier, value in module_tiers.items():
            if tier not in {"t1", "t2", "t3"}:
                warnings.append(f"unknown module tier override ignored: {module.get('name', index)}.{tier}")
                continue
            if not isinstance(value, dict):
                errors.append(f"project.modules[{index}].testing.tiers.{tier} must be an object")
                continue
            commands = value.get("commands", [])
            if not isinstance(commands, list):
                errors.append(f"project.modules[{index}].testing.tiers.{tier}.commands must be an array")
            else:
                for command_index, command in enumerate(commands):
                    _validate_command(command, f"project.modules[{index}].testing.tiers.{tier}.commands[{command_index}]", errors)

    return {"valid": not errors, "errors": errors, "warnings": warnings}


def load_config(root: Path, path: Path | None = None, *, required: bool = False) -> dict[str, Any]:
    root = root.resolve()
    config_path = path.resolve() if path else root / ".siyrs" / "config.yaml"
    if not config_path.exists():
        if required:
            raise ConfigError(f"configuration file not found: {config_path}")
        data = deepcopy(DEFAULT_CONFIG)
        result = validate_config(data, root)
        return {"path": str(config_path), "exists": False, "config": data, **result}
    raw = parse_yaml_subset(config_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ConfigError("configuration root must be a mapping")
    data = _merge(DEFAULT_CONFIG, raw)
    result = validate_config(data, root)
    return {"path": str(config_path), "exists": True, "config": data, **result}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and normalize .siyrs/config.yaml")
    parser.add_argument("--root", default=".")
    parser.add_argument("--file")
    parser.add_argument("--required", action="store_true")
    args = parser.parse_args()
    try:
        result = load_config(Path(args.root), Path(args.file) if args.file else None, required=args.required)
    except (OSError, ConfigError) as exc:
        result = {"valid": False, "errors": [str(exc)], "warnings": []}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("valid") else 1


if __name__ == "__main__":
    raise SystemExit(main())
