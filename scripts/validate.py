#!/usr/bin/env python3
"""Siyrs Skill 套件的轻量结构校验器。"""

from __future__ import annotations

import re
import sys
from pathlib import Path

NAME_RE = re.compile(r"^[a-z0-9-]{1,64}$")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
QUOTED_FIELD_RE = re.compile(
    r'^\s{2}(display_name|short_description|default_prompt):\s+"([^"]+)"\s*$',
    re.MULTILINE,
)
LEGACY_PATHS = ("adapters", "commands", "schemas", "release-manifest.json")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md 必须以 YAML frontmatter 开始")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("SKILL.md 的 frontmatter 未闭合") from exc

    data: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"不支持的 frontmatter 行：{line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def discover_skill_dirs(root: Path) -> list[tuple[Path, bool]]:
    """发现根 Skill 与 skills/ 下全部一级子 Skill。"""
    discovered: list[tuple[Path, bool]] = [(root, False)]
    skill_root = root / "skills"
    if not skill_root.is_dir():
        return discovered

    for child in sorted(skill_root.iterdir(), key=lambda path: path.name):
        if child.is_dir():
            discovered.append((child, True))
    return discovered


def validate_skill(skill_dir: Path, *, explicit_child: bool = False) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return [f"缺少 {skill_path}"]

    text = skill_path.read_text(encoding="utf-8")
    try:
        meta = parse_frontmatter(text)
        if set(meta) != {"name", "description"}:
            raise ValueError("frontmatter 只能包含 name 和 description")
        if not NAME_RE.fullmatch(meta["name"]):
            raise ValueError("name 必须使用小写连字符格式，且不超过 64 个字符")
        if not meta["description"]:
            raise ValueError("description 不能为空")
        if explicit_child and meta["name"] != skill_dir.name:
            raise ValueError("子 Skill 的 name 必须与目录名一致")
    except (KeyError, ValueError) as exc:
        errors.append(f"{skill_path}: {exc}")
        meta = {}

    if len(text.splitlines()) > 500:
        errors.append(f"{skill_path}: 必须保持在 500 行以内")

    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "#")):
            continue
        if not (skill_dir / target).is_file():
            errors.append(f"{skill_path}: 链接目标不存在 {target}")

    agent_path = skill_dir / "agents" / "openai.yaml"
    if not agent_path.is_file():
        errors.append(f"{skill_dir}: 缺少 agents/openai.yaml")
    else:
        agent_text = agent_path.read_text(encoding="utf-8")
        fields = dict(QUOTED_FIELD_RE.findall(agent_text))
        for field in ("display_name", "short_description", "default_prompt"):
            if field not in fields:
                errors.append(f"{agent_path}: 缺少带双引号的 interface.{field}")
        short = fields.get("short_description", "")
        if short and not (25 <= len(short) <= 64):
            errors.append(f"{agent_path}: short_description 长度必须为 25-64 个字符")
        name = meta.get("name")
        if name and f"${name}" not in fields.get("default_prompt", ""):
            errors.append(f"{agent_path}: default_prompt 必须明确包含 ${name}")
        if explicit_child and "allow_implicit_invocation: false" not in agent_text:
            errors.append(f"{agent_path}: skills/ 下子 Skill 必须关闭隐式调用")

    refs = skill_dir / "references"
    if refs.exists() and any(p.is_dir() for p in refs.rglob("*")):
        errors.append(f"{refs}: references 必须保持一层深度")

    return errors


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    for skill_dir, explicit_child in discover_skill_dirs(root):
        errors.extend(validate_skill(skill_dir, explicit_child=explicit_child))

    for legacy in LEGACY_PATHS:
        if (root / legacy).exists():
            errors.append(f"旧运行时层必须继续保持删除状态：{legacy}")

    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        return 1
    print("Skill 套件校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
