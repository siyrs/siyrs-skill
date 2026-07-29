#!/usr/bin/env python3
"""Normalize siyrs-skill slash commands and Chinese aliases."""
from __future__ import annotations

import argparse
import json
import shlex
from dataclasses import asdict, dataclass, field

TEST_COMMANDS = {
    "/siyk-test-add": "standard",
    "/siyk-test-run-t1": None,
    "/siyk-test-run-t2": "quick",
    "/siyk-test-run-t3": "strict",
}
VALID_STRENGTHS = {"quick", "standard", "strict"}
ADD_ALIASES = ("沉淀测试", "沉淀")
T1_ALIASES = ("跑t1", "变更回测", "跑改动相关的测试", "change regression", "regression")
T2_ALIASES = ("跑t2", "冒烟", "smoke")
T3_ALIASES = ("跑t3", "全量沉淀测试", "完整沉淀测试", "全量沉淀", "全量", "release gate", "full")
COMMIT_ALIASES = ("保存本地代码", "本地保存代码", "本地保存", "本地提交")
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


def _is_allow_risk(token: str) -> bool:
    return token == "--allow-risk" or token.startswith("--allow-risk=")


def route(text: str) -> dict:
    raw = text.strip()
    if not raw:
        return asdict(RouteResult(matched=False))
    tokens = _split(raw)
    first = tokens[0] if tokens else ""

    if first in TEST_COMMANDS:
        rest = tokens[1:]
        strength = TEST_COMMANDS[first]
        if rest and rest[0] in VALID_STRENGTHS:
            strength = rest.pop(0)
        extra = " ".join(rest)
        parts = [first]
        if strength:
            parts.append(strength)
        if extra:
            parts.append(extra)
        normalized = " ".join(parts)
        return asdict(RouteResult(True, command=first, strength=strength, extra=extra, normalized=normalized, source="literal"))

    if first == "/siyk-git-commit":
        flags, extra_tokens, warnings = [], [], []
        for token in tokens[1:]:
            if token == "--no-test" or _is_allow_risk(token):
                if token not in flags:
                    flags.append(token)
            elif token.startswith("--"):
                warnings.append(f"unknown flag: {token}")
                extra_tokens.append(token)
            else:
                extra_tokens.append(token)
        parts = [first, *flags, *extra_tokens]
        return asdict(RouteResult(True, command=first, flags=flags, extra=" ".join(extra_tokens), normalized=" ".join(parts), source="literal", warnings=warnings))

    if first == "/siyk-git-sync":
        branch = None
        flags, extra_tokens, warnings = [], [], []
        for token in tokens[1:]:
            if token in {"--pr", "--no-test"} or _is_allow_risk(token):
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
        return asdict(RouteResult(True, command=first, branch=branch, flags=flags, extra=" ".join(extra_tokens), normalized=" ".join(parts), source="literal", warnings=warnings))

    for aliases, command, strength in (
        (T3_ALIASES, "/siyk-test-run-t3", "strict"),
        (T2_ALIASES, "/siyk-test-run-t2", "quick"),
        (T1_ALIASES, "/siyk-test-run-t1", None),
        (ADD_ALIASES, "/siyk-test-add", "standard"),
    ):
        alias = _matches_alias(raw, aliases)
        if alias:
            extra = raw[len(alias):].strip()
            parts = [command]
            if strength:
                parts.append(strength)
            if extra:
                parts.append(extra)
            normalized = " ".join(parts)
            return asdict(RouteResult(True, command=command, strength=strength, extra=extra, normalized=normalized, source=f"alias:{alias}"))

    for aliases, command in ((COMMIT_ALIASES, "/siyk-git-commit"), (SYNC_ALIASES, "/siyk-git-sync")):
        alias = _matches_alias(raw, aliases)
        if alias:
            extra = raw[len(alias):].strip()
            normalized = command + (f" {extra}" if extra else "")
            routed = route(normalized)
            routed["source"] = f"alias:{alias}"
            return routed

    return asdict(RouteResult(matched=False))


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize a siyrs-skill command")
    parser.add_argument("text")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()
    result = route(args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0 if result["matched"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
