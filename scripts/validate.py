#!/usr/bin/env python3
"""Siyrs Skill Agent Skills Collection 的轻量结构校验器。"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from install import build_claude_skills  # noqa: E402
from sync_references import discover_skill_dirs, reference_sync_errors  # noqa: E402

NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
QUOTED_FIELD_RE = re.compile(
    r'^\s{2}(display_name|short_description|default_prompt):\s+"([^"]+)"\s*$',
    re.MULTILINE,
)
ALLOWED_FRONTMATTER_FIELDS = {
    "name",
    "description",
    "license",
    "allowed-tools",
    "metadata",
    "compatibility",
}
FORBIDDEN_COLLECTION_ROOTS = (
    "SKILL.md",
    "agents",
    "references",
    ".claude-plugin",
    "adapters",
    "commands",
    "schemas",
    "release-manifest.json",
)


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
        if line.startswith((" ", "\t")):
            # 当前仓库不使用嵌套 metadata；让官方 validator 负责通用 YAML 结构。
            continue
        if ":" not in line:
            raise ValueError(f"不支持的 frontmatter 行：{line}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _validate_markdown_links(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    markdown_files = [skill_dir / "SKILL.md"]
    refs = skill_dir / "references"
    if refs.is_dir():
        markdown_files.extend(sorted(refs.rglob("*.md")))

    for markdown in markdown_files:
        text = markdown.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split("#", 1)[0].split("?", 1)[0]
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            candidate = (markdown.parent / target).resolve()
            if not _is_within(candidate, skill_dir):
                errors.append(f"{markdown}: 本地链接越过 Skill 根目录：{raw_target}")
            elif not candidate.is_file():
                errors.append(f"{markdown}: 链接目标不存在：{raw_target}")
    return errors


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return [f"缺少 {skill_path}"]

    text = skill_path.read_text(encoding="utf-8")
    try:
        meta = parse_frontmatter(text)
        unexpected = set(meta) - ALLOWED_FRONTMATTER_FIELDS
        if unexpected:
            raise ValueError(f"frontmatter 含非 Agent Skills 标准字段：{', '.join(sorted(unexpected))}")
        if not meta.get("name") or not meta.get("description"):
            raise ValueError("frontmatter 必须包含非空 name 和 description")
        name = meta["name"]
        if len(name) > 64 or not NAME_RE.fullmatch(name):
            raise ValueError("name 必须为不超过 64 字符的小写连字符格式")
        if name != skill_dir.name:
            raise ValueError("Skill 的 name 必须与父目录名一致")
        description = meta["description"]
        if len(description) > 1024:
            raise ValueError("description 不能超过 1024 字符")
        if name.startswith("siyk-") and len(description) > 80:
            raise ValueError("显式 siyk-* Skill 的 description 应保持在 80 字符以内")
        if "disable-model-invocation" in text.split("---", 2)[1]:
            raise ValueError("严格 Agent Skills 源包不能包含 Claude 专用字段")
    except ValueError as exc:
        errors.append(f"{skill_path}: {exc}")
        meta = {}

    if len(text.splitlines()) > 500:
        errors.append(f"{skill_path}: 必须保持在 500 行以内")
    if "../../references" in text or "../references" in text:
        errors.append(f"{skill_path}: 独立 Skill 不能依赖 Skill 根目录外的 references")
    if (skill_dir / "skills").exists():
        errors.append(f"{skill_dir}: 独立 Skill 内不能继续嵌套 skills/")

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
        if short and not (15 <= len(short) <= 64):
            errors.append(f"{agent_path}: short_description 长度必须为 15-64 个字符")
        name = meta.get("name")
        if name and f"${name}" not in fields.get("default_prompt", ""):
            errors.append(f"{agent_path}: default_prompt 必须明确包含 ${name}")
        expected_policy = "true" if skill_dir.name == "siyrs-skill" else "false"
        if f"allow_implicit_invocation: {expected_policy}" not in agent_text:
            errors.append(
                f"{agent_path}: allow_implicit_invocation 必须为 {expected_policy}"
            )

    refs = skill_dir / "references"
    if refs.exists() and any(path.is_dir() for path in refs.rglob("*")):
        errors.append(f"{refs}: references 必须保持一层深度")

    errors.extend(_validate_markdown_links(skill_dir))
    return errors



def validate_claude_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_path = skill_dir / "SKILL.md"
    if not skill_path.is_file():
        return [f"Claude 变体缺少 {skill_path}"]
    try:
        meta = parse_frontmatter(skill_path.read_text(encoding="utf-8"))
    except ValueError as exc:
        return [f"{skill_path}: {exc}"]

    allowed = ALLOWED_FRONTMATTER_FIELDS | {"disable-model-invocation"}
    unexpected = set(meta) - allowed
    if unexpected:
        errors.append(f"{skill_path}: Claude 变体含未知字段：{sorted(unexpected)}")
    if meta.get("name") != skill_dir.name:
        errors.append(f"{skill_path}: Claude 变体 name 与目录不一致")
    if skill_dir.name.startswith("siyk-"):
        if meta.get("disable-model-invocation") != "true":
            errors.append(f"{skill_path}: 显式 Skill 必须关闭 Claude 模型调用")
    elif "disable-model-invocation" in meta:
        errors.append(f"{skill_path}: 主 Skill 必须保持 Claude 可自动调用")
    if (skill_dir / "agents").exists():
        errors.append(f"{skill_dir}: Claude 变体不应包含 Codex agents 元数据")
    errors.extend(_validate_markdown_links(skill_dir))
    return errors

def validate(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for forbidden in FORBIDDEN_COLLECTION_ROOTS:
        if (root / forbidden).exists():
            errors.append(f"Collection 根目录不应存在运行时入口：{forbidden}")

    shared_root = root / "shared" / "references"
    if not shared_root.is_dir():
        errors.append("缺少 shared/references 共享 Markdown 源")
    elif any(path.is_dir() for path in shared_root.rglob("*")):
        errors.append("shared/references 必须保持一层深度")

    skill_dirs = discover_skill_dirs(root)
    if not skill_dirs:
        errors.append("skills/ 下没有发现独立 Agent Skill")
        return errors
    if not (root / "skills" / "siyrs-skill" / "SKILL.md").is_file():
        errors.append("缺少主 Skill：skills/siyrs-skill/SKILL.md")

    for skill_dir in skill_dirs:
        errors.extend(validate_skill(skill_dir))

    errors.extend(reference_sync_errors(root))

    if not errors:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "claude" / "skills"
            try:
                built = build_claude_skills(root, output)
            except (OSError, RuntimeError, ValueError) as exc:
                errors.append(f"Claude 变体生成失败：{exc}")
            else:
                if {path.name for path in built} != {path.name for path in skill_dirs}:
                    errors.append("Claude 变体 Skill 集合与源码不一致")
                for skill_dir in built:
                    errors.extend(validate_claude_skill(skill_dir))
    return errors


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    errors = validate(root)
    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        return 1
    print("Agent Skills Collection 校验通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
