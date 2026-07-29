#!/usr/bin/env python3
"""Load siyrs-skill command metadata from Markdown frontmatter.

Command Markdown is the single source of truth for command names, kinds, tiers,
strengths, aliases, legacy commands, and client discovery behavior.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.S)
REQUIRED_KEYS = {
    "command",
    "order",
    "kind",
    "strengths",
    "default_strength",
    "aliases_prefix",
    "aliases_exact",
    "legacy_commands",
    "client_entrypoint",
}


@dataclass(frozen=True)
class CommandSpec:
    path: str
    order: int
    command: str
    kind: str
    tier: str | None
    strengths: tuple[str, ...]
    default_strength: str | None
    aliases_prefix: tuple[str, ...]
    aliases_exact: tuple[str, ...]
    legacy_commands: tuple[str, ...]
    client_entrypoint: bool
    deprecated_message: str | None = None

    @property
    def name(self) -> str:
        return self.command.removeprefix("/")

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "order": self.order,
            "command": self.command,
            "name": self.name,
            "kind": self.kind,
            "tier": self.tier,
            "strengths": list(self.strengths),
            "default_strength": self.default_strength,
            "aliases_prefix": list(self.aliases_prefix),
            "aliases_exact": list(self.aliases_exact),
            "legacy_commands": list(self.legacy_commands),
            "client_entrypoint": self.client_entrypoint,
            "deprecated_message": self.deprecated_message,
        }


def _parse_value(raw: str) -> Any:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False
        if raw.lower() in {"null", "none", "~"}:
            return None
        return raw.strip('"\'')


def parse_frontmatter(path: Path, required_keys: set[str] | None = None) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError(f"frontmatter missing or malformed: {path}")
    metadata: dict[str, Any] = {}
    for lineno, line in enumerate(match.group(1).splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line {lineno} in {path}: {line!r}")
        key, raw = line.split(":", 1)
        key = key.strip()
        if key in metadata:
            raise ValueError(f"duplicate frontmatter key {key!r}: {path}")
        metadata[key] = _parse_value(raw)
    required = REQUIRED_KEYS if required_keys is None else required_keys
    missing = sorted(required - metadata.keys())
    if missing:
        raise ValueError(f"missing command metadata {missing}: {path}")
    return metadata, text[match.end():]


def _string_tuple(value: Any, key: str, path: Path) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{key} must be a non-empty-string array: {path}")
    return tuple(value)


def load_registry(root: Path) -> list[CommandSpec]:
    root = root.resolve()
    command_dir = root / "commands"
    specs: list[CommandSpec] = []
    for path in sorted(command_dir.glob("*.md")):
        metadata, _ = parse_frontmatter(path, REQUIRED_KEYS)
        command = metadata["command"]
        if not isinstance(command, str) or not re.fullmatch(r"/siyk-[a-z0-9-]+", command):
            raise ValueError(f"invalid command name {command!r}: {path}")
        strengths = _string_tuple(metadata["strengths"], "strengths", path) if metadata["strengths"] else ()
        aliases_prefix = _string_tuple(metadata["aliases_prefix"], "aliases_prefix", path) if metadata["aliases_prefix"] else ()
        aliases_exact = _string_tuple(metadata["aliases_exact"], "aliases_exact", path) if metadata["aliases_exact"] else ()
        legacy_commands = _string_tuple(metadata["legacy_commands"], "legacy_commands", path) if metadata["legacy_commands"] else ()
        default_strength = metadata["default_strength"]
        if default_strength is not None and default_strength not in strengths:
            raise ValueError(f"default_strength must be listed in strengths: {path}")
        if not isinstance(metadata["client_entrypoint"], bool):
            raise ValueError(f"client_entrypoint must be boolean: {path}")
        tier = metadata.get("tier")
        if tier is not None and tier not in {"T1", "T2", "T3"}:
            raise ValueError(f"invalid tier {tier!r}: {path}")
        order = metadata["order"]
        if not isinstance(order, int):
            raise ValueError(f"order must be integer: {path}")
        specs.append(CommandSpec(
            path=path.relative_to(root).as_posix(),
            order=order,
            command=command,
            kind=str(metadata["kind"]),
            tier=tier,
            strengths=strengths,
            default_strength=default_strength,
            aliases_prefix=aliases_prefix,
            aliases_exact=aliases_exact,
            legacy_commands=legacy_commands,
            client_entrypoint=metadata["client_entrypoint"],
            deprecated_message=metadata.get("deprecated_message"),
        ))
    _validate_registry(specs)
    return sorted(specs, key=lambda spec: spec.order)


def _normalized_alias(value: str) -> str:
    return " ".join(value.strip().casefold().split())


def _validate_registry(specs: Iterable[CommandSpec]) -> None:
    specs = list(specs)
    commands: dict[str, str] = {}
    orders: dict[int, str] = {}
    aliases: dict[str, str] = {}
    legacy: dict[str, str] = {}
    for spec in specs:
        if spec.order in orders:
            raise ValueError(f"duplicate command order {spec.order}: {orders[spec.order]} and {spec.path}")
        orders[spec.order] = spec.path
        if spec.command in commands:
            raise ValueError(f"duplicate command {spec.command}: {commands[spec.command]} and {spec.path}")
        commands[spec.command] = spec.path
        for alias in (*spec.aliases_prefix, *spec.aliases_exact):
            key = _normalized_alias(alias)
            if key in aliases and aliases[key] != spec.command:
                raise ValueError(f"alias collision {alias!r}: {aliases[key]} and {spec.command}")
            aliases[key] = spec.command
        for old in spec.legacy_commands:
            if not re.fullmatch(r"/siyk-[a-z0-9-]+", old):
                raise ValueError(f"invalid legacy command {old!r}: {spec.path}")
            if old in commands or old in legacy:
                raise ValueError(f"legacy command collision: {old}")
            legacy[old] = spec.command


def registry_document(root: Path) -> dict[str, Any]:
    specs = load_registry(root)
    return {
        "commands": [spec.to_dict() for spec in specs],
        "current_commands": [spec.command for spec in specs],
        "entrypoint_names": [spec.name for spec in specs if spec.client_entrypoint],
        "legacy_commands": sorted({old for spec in specs for old in spec.legacy_commands}),
        "legacy_names": sorted({old.removeprefix('/') for spec in specs for old in spec.legacy_commands}),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Read Markdown-first siyrs-skill command registry")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--field", choices=["json", "commands", "names", "legacy", "legacy-names"], default="json")
    args = parser.parse_args()
    try:
        doc = registry_document(Path(args.root))
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False, indent=2))
        return 1
    field_map = {
        "commands": "current_commands",
        "names": "entrypoint_names",
        "legacy": "legacy_commands",
        "legacy-names": "legacy_names",
    }
    if args.field == "json":
        print(json.dumps(doc, ensure_ascii=False, indent=2))
    else:
        for item in doc[field_map[args.field]]:
            print(item)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
