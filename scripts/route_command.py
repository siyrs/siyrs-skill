#!/usr/bin/env python3
"""Normalize siyrs-skill slash commands and Chinese aliases.

This parser is intentionally conservative. It only routes commands at the start of
an input string and returns evidence for the agent; it does not execute workflows.
"""
from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import asdict, dataclass, field

TEST_COMMANDS = {
    "/siyk-test-full": "strict",
    "/siyk-test-new": "standard",
}
VALID_STRENGTHS = {"quick", "standard", "strict"}
FULL_ALIASES = ("全量沉淀测试", "完整沉淀测试", "全量沉淀")
NEW_ALIASES = ("沉淀测试", "沉淀")
SYNC_ALIASES = ("保存并同步远程仓库", "同步代码")


@dataclass
class RouteResult:
    matched: bool
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


def _matches_alias(text: str, aliases: tuple[str, ...]) -> str | None:
    for alias in aliases:
        if text == alias or text.startswith(alias + " "):
            return alias
    return None


def route(text: str) -> dict:
    raw = text.strip()
    if not raw:
        return asdict(RouteResult(matched=False))

    tokens = _split(raw)
    first = tokens[0] if tokens else ""

    if first in TEST_COMMANDS:
        default_strength = TEST_COMMANDS[first]
        strength = default_strength
        rest = tokens[1:]
        if rest and rest[0] in VALID_STRENGTHS:
            strength = rest.pop(0)
        extra = " ".join(rest)
        normalized = f"{first} {strength}" + (f" {extra}" if extra else "")
        return asdict(RouteResult(
            matched=True,
            command=first,
            strength=strength,
            extra=extra,
            normalized=normalized,
            source="literal",
        ))

    if first == "/siyk-git-sync":
        branch = None
        flags: list[str] = []
        extra_tokens: list[str] = []
        warnings: list[str] = []
        for token in tokens[1:]:
            if token in {"--pr", "--no-test"}:
                if token not in flags:
                    flags.append(token)
            elif token.startswith("--"):
                warnings.append(f"unknown flag: {token}")
                extra_tokens.append(token)
            elif branch is None:
                branch = token
            else:
                extra_tokens.append(token)
        parts = [first]
        if branch:
            parts.append(branch)
        parts.extend(flags)
        parts.extend(extra_tokens)
        return asdict(RouteResult(
            matched=True,
            command=first,
            branch=branch,
            flags=flags,
            extra=" ".join(extra_tokens),
            normalized=" ".join(parts),
            source="literal",
            warnings=warnings,
        ))

    alias = _matches_alias(raw, FULL_ALIASES)
    if alias:
        extra = raw[len(alias):].strip()
        normalized = "/siyk-test-full strict" + (f" {extra}" if extra else "")
        return asdict(RouteResult(
            matched=True,
            command="/siyk-test-full",
            strength="strict",
            extra=extra,
            normalized=normalized,
            source=f"alias:{alias}",
        ))

    alias = _matches_alias(raw, NEW_ALIASES)
    if alias:
        extra = raw[len(alias):].strip()
        normalized = "/siyk-test-new standard" + (f" {extra}" if extra else "")
        return asdict(RouteResult(
            matched=True,
            command="/siyk-test-new",
            strength="standard",
            extra=extra,
            normalized=normalized,
            source=f"alias:{alias}",
        ))

    alias = _matches_alias(raw, SYNC_ALIASES)
    if alias:
        extra = raw[len(alias):].strip()
        normalized = "/siyk-git-sync" + (f" {extra}" if extra else "")
        return asdict(RouteResult(
            matched=True,
            command="/siyk-git-sync",
            extra=extra,
            normalized=normalized,
            source=f"alias:{alias}",
        ))

    return asdict(RouteResult(matched=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a siyrs-skill command")
    parser.add_argument("text", help="Literal slash command or supported Chinese alias")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = route(args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result["matched"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
