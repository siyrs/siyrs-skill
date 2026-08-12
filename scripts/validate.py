#!/usr/bin/env python3
"""Lightweight structural validation for the SIYRS Agent Skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
QUOTED_FIELD_RE = re.compile(r'^\s{2}(display_name|short_description|default_prompt):\s+"([^"]+)"\s*$', re.MULTILINE)
LEGACY_PATHS = (
    "adapters",
    "commands",
    "schemas",
    "release-manifest.json",
)


def fail(message: str) -> None:
    raise ValueError(message)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail("SKILL.md must start with YAML frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter is not closed") from exc

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            fail(f"unsupported frontmatter line: {line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    skill_path = root / "SKILL.md"
    if not skill_path.is_file():
        return ["missing SKILL.md"]

    text = skill_path.read_text(encoding="utf-8")
    try:
        meta = parse_frontmatter(text)
        if set(meta) != {"name", "description"}:
            fail("frontmatter must contain only name and description")
        if not NAME_RE.fullmatch(meta["name"]):
            fail("name must be lowercase hyphen-case and <=64 characters")
        if not meta["description"]:
            fail("description must be non-empty")
    except (KeyError, ValueError) as exc:
        errors.append(str(exc))
        meta = {}

    if len(text.splitlines()) > 500:
        errors.append("SKILL.md must stay under 500 lines")

    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (root / target).is_file():
            errors.append(f"broken SKILL.md link: {target}")

    agent_path = root / "agents" / "openai.yaml"
    if not agent_path.is_file():
        errors.append("missing agents/openai.yaml")
    else:
        agent_text = agent_path.read_text(encoding="utf-8")
        fields = dict(QUOTED_FIELD_RE.findall(agent_text))
        for field in ("display_name", "short_description", "default_prompt"):
            if field not in fields:
                errors.append(f"agents/openai.yaml missing quoted interface.{field}")
        short = fields.get("short_description", "")
        if short and not (25 <= len(short) <= 64):
            errors.append("interface.short_description must be 25-64 characters")
        name = meta.get("name")
        if name and f"${name}" not in fields.get("default_prompt", ""):
            errors.append("interface.default_prompt must explicitly mention $skill-name")

    refs = root / "references"
    if refs.exists():
        nested = [p for p in refs.rglob("*") if p.is_dir() and p != refs]
        if nested:
            errors.append("references must stay one level deep")

    for legacy in LEGACY_PATHS:
        if (root / legacy).exists():
            errors.append(f"legacy runtime layer must stay removed: {legacy}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Skill validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
