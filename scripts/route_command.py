#!/usr/bin/env python3
"""Normalize siyrs-skill commands from Markdown command metadata."""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from dataclasses import asdict, dataclass, field
from pathlib import Path

from command_registry import CommandSpec, load_registry

GLOBAL_STRENGTHS = {"quick", "standard", "strict"}


@dataclass
class RouteResult:
    matched: bool
    valid: bool = True
    command: str | None = None
    strength: str | None = None
    branch: str | None = None
    flags: list[str] = field(default_factory=list)
    extra: str = ""
    normalized: str | None = None
    source: str | None = None
    warnings: list[str] = field(default_factory=list)


def _split(text: str) -> list[str]:
    try:
        return shlex.split(text, posix=True)
    except ValueError:
        return text.split()


def _norm(text: str) -> str:
    return " ".join(text.strip().casefold().split())


def _registry(root: Path | None = None) -> list[CommandSpec]:
    return load_registry(root or Path(__file__).resolve().parents[1])


def _route_test(spec: CommandSpec, tokens: list[str], *, source: str, warnings: list[str] | None = None) -> dict:
    rest = list(tokens)
    warnings = list(warnings or [])
    strength = spec.default_strength
    valid = True
    if rest and rest[0].casefold() in GLOBAL_STRENGTHS:
        candidate = rest.pop(0).casefold()
        if candidate in spec.strengths:
            strength = candidate
        else:
            valid = False
            warnings.append(f"strength {candidate!r} is not supported by {spec.command}")
    extra = " ".join(rest)
    parts = [spec.command]
    if strength:
        parts.append(strength)
    if extra:
        parts.append(extra)
    return asdict(RouteResult(
        matched=True,
        valid=valid,
        command=spec.command,
        strength=strength,
        extra=extra,
        normalized=" ".join(parts),
        source=source,
        warnings=warnings,
    ))


def _is_allow_risk(token: str) -> bool:
    return token == "--allow-risk" or token.startswith("--allow-risk=")


def _valid_branch_name(value: str) -> bool:
    if not value:
        return False
    completed = subprocess.run(
        ["git", "check-ref-format", "--branch", value],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return completed.returncode == 0


def _route_git(spec: CommandSpec, tokens: list[str], *, source: str, warnings: list[str] | None = None) -> dict:
    warnings = list(warnings or [])
    flags: list[str] = []
    extra: list[str] = []
    branch: str | None = None
    valid = True
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--no-test":
            if token not in flags:
                flags.append(token)
                warnings.append("--no-test is retained for compatibility; Git workflows already disable tests by default")
        elif _is_allow_risk(token) or (spec.command == "/siyk-git-sync" and token == "--pr"):
            if token not in flags:
                flags.append(token)
        elif spec.command == "/siyk-git-sync" and token == "--branch":
            index += 1
            if index >= len(tokens):
                warnings.append("--branch requires a value")
                valid = False
            elif branch is not None:
                warnings.append("--branch may only be supplied once")
                valid = False
            else:
                branch = tokens[index]
        elif spec.command == "/siyk-git-sync" and token.startswith("--branch="):
            candidate = token.split("=", 1)[1]
            if branch is not None:
                warnings.append("--branch may only be supplied once")
                valid = False
            else:
                branch = candidate
        elif token.startswith("--"):
            warnings.append(f"unknown flag: {token}")
            valid = False
            extra.append(token)
        else:
            # Positional text is always supplemental intent. Branch selection is explicit-only.
            extra.append(token)
        index += 1

    if branch is not None and not _valid_branch_name(branch):
        warnings.append(f"invalid Git branch name: {branch!r}")
        valid = False

    parts = [spec.command]
    if branch:
        parts.extend(["--branch", branch])
    parts.extend(flags)
    parts.extend(extra)
    return asdict(RouteResult(
        matched=True,
        valid=valid,
        command=spec.command,
        branch=branch,
        flags=flags,
        extra=" ".join(extra),
        normalized=" ".join(parts),
        source=source,
        warnings=warnings,
    ))


def _route_spec(spec: CommandSpec, tokens: list[str], source: str, warnings: list[str] | None = None) -> dict:
    if spec.kind.startswith("test"):
        return _route_test(spec, tokens, source=source, warnings=warnings)
    return _route_git(spec, tokens, source=source, warnings=warnings)


def route(text: str, root: Path | None = None) -> dict:
    raw = text.strip()
    if not raw:
        return asdict(RouteResult(matched=False))
    specs = _registry(root)
    by_command = {spec.command: spec for spec in specs}
    legacy = {old: spec for spec in specs for old in spec.legacy_commands}
    tokens = _split(raw)
    first = tokens[0] if tokens else ""

    if first in by_command:
        return _route_spec(by_command[first], tokens[1:], "literal")
    if first in legacy:
        spec = legacy[first]
        rest = tokens[1:]
        warnings = [spec.deprecated_message or f"{first} is deprecated; use {spec.command}"]
        if first == "/siyk-test-full" and rest and rest[0].casefold() in GLOBAL_STRENGTHS:
            old_strength = rest.pop(0).casefold()
            warnings.append(f"legacy strength {old_strength!r} is ignored; T3 is always strict")
        return _route_spec(spec, rest, f"legacy:{first}", warnings)

    normalized_raw = _norm(raw)
    exact_matches: list[tuple[CommandSpec, str]] = []
    prefix_matches: list[tuple[CommandSpec, str, str]] = []
    for spec in specs:
        for alias in spec.aliases_exact:
            if normalized_raw == _norm(alias):
                exact_matches.append((spec, alias))
        for alias in spec.aliases_prefix:
            key = _norm(alias)
            if normalized_raw == key:
                prefix_matches.append((spec, alias, ""))
            elif normalized_raw.startswith(key + " "):
                prefix_matches.append((spec, alias, normalized_raw[len(key):].strip()))
    if exact_matches:
        spec, alias = exact_matches[0]
        return _route_spec(spec, [], f"alias:{alias}")
    if prefix_matches:
        spec, alias, remainder = sorted(prefix_matches, key=lambda item: len(_norm(item[1])), reverse=True)[0]
        return _route_spec(spec, _split(remainder), f"alias:{alias}")
    return asdict(RouteResult(matched=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a siyrs-skill command")
    parser.add_argument("text")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    try:
        result = route(args.text, Path(args.root))
    except (OSError, ValueError) as exc:
        result = asdict(RouteResult(matched=False, valid=False, warnings=[str(exc)]))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    if not result["matched"]:
        return 1
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
