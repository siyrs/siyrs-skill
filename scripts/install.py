#!/usr/bin/env python3
"""将 Siyrs Skill Collection 安装为 Codex 与 Claude Code 的平级 Agent Skills。"""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from sync_references import discover_skill_dirs, reference_sync_errors  # noqa: E402


def _frontmatter_with_claude_policy(text: str, *, explicit_only: bool) -> str:
    if not explicit_only:
        return text
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md 缺少 frontmatter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("SKILL.md frontmatter 未闭合") from exc
    if any(line.split(":", 1)[0].strip() == "disable-model-invocation" for line in lines[1:end]):
        return text
    lines.insert(end, "disable-model-invocation: true")
    suffix = "\n" if text.endswith("\n") else ""
    return "\n".join(lines) + suffix


def build_claude_skills(source_root: Path, output_root: Path) -> list[Path]:
    source_root = source_root.resolve()
    output_root = output_root.resolve()
    sync_errors = reference_sync_errors(source_root)
    if sync_errors:
        raise RuntimeError("共享 reference 未同步：\n" + "\n".join(sync_errors))

    if output_root == source_root or output_root == output_root.parent:
        raise ValueError(f"拒绝把 Claude 生成目录指向危险路径：{output_root}")
    if output_root.exists():
        shutil.rmtree(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    built: list[Path] = []
    for source in discover_skill_dirs(source_root):
        target = output_root / source.name
        shutil.copytree(
            source,
            target,
            ignore=shutil.ignore_patterns("agents", "__pycache__", "*.pyc"),
        )
        skill_path = target / "SKILL.md"
        skill_path.write_text(
            _frontmatter_with_claude_policy(
                skill_path.read_text(encoding="utf-8"),
                explicit_only=source.name.startswith("siyk-"),
            ),
            encoding="utf-8",
        )
        built.append(target)
    return built


def _lexists(path: Path) -> bool:
    return os.path.lexists(path)


def _is_junction(path: Path) -> bool:
    checker = getattr(os.path, "isjunction", None)
    if checker and checker(path):
        return True
    if os.name != "nt" or not _lexists(path):
        return False
    try:
        attributes = os.lstat(path).st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT) and path.is_dir()


def _is_link_like(path: Path) -> bool:
    return path.is_symlink() or _is_junction(path)


def _same_target(link: Path, target: Path) -> bool:
    try:
        return _lexists(link) and target.exists() and os.path.samefile(link, target)
    except OSError:
        return False


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def ensure_neutral_source(source_root: Path, home: Path) -> None:
    source_root = source_root.resolve()
    for host_root in (home / ".agents" / "skills", home / ".claude" / "skills"):
        if _is_within(source_root, host_root):
            raise RuntimeError(
                "Collection 源码不能位于 Codex / Claude Code 的 Skill 搜索目录内。"
                "请迁移到中立路径，例如 $HOME/.siyrs/siyrs-skill。"
            )


def _remove_link_only(path: Path) -> None:
    if path.is_symlink():
        path.unlink()
    elif _is_junction(path):
        path.rmdir()
    else:
        raise RuntimeError(f"拒绝删除非链接目录：{path}")


def _create_directory_link(link: Path, target: Path) -> None:
    link.parent.mkdir(parents=True, exist_ok=True)
    if os.name == "nt":
        completed = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise RuntimeError(f"创建 Junction 失败：{link} -> {target}\n{detail}")
    else:
        link.symlink_to(target, target_is_directory=True)


def ensure_link(link: Path, target: Path, *, repair_links: bool) -> str:
    target = target.resolve()
    if not target.is_dir():
        raise RuntimeError(f"Skill 目标目录不存在：{target}")
    if _same_target(link, target):
        return "ok"
    if _lexists(link):
        if repair_links and _is_link_like(link):
            _remove_link_only(link)
        else:
            kind = "旧链接" if _is_link_like(link) else "真实目录/文件"
            raise RuntimeError(
                f"安装目标已被{kind}占用：{link}\n"
                "请先确认来源；仅链接可使用 --repair-links 安全替换，真实目录不会自动删除。"
            )
    _create_directory_link(link, target)
    return "created"


def desired_targets(
    source_root: Path, home: Path, target: str, *, prepare_claude: bool
) -> dict[Path, Path]:
    source_root = source_root.resolve()
    skills = discover_skill_dirs(source_root)
    if target == "codex":
        root = home / ".agents" / "skills"
        return {root / skill.name: skill.resolve() for skill in skills}
    if target == "claude":
        generated = source_root / ".generated" / "claude" / "skills"
        if prepare_claude:
            build_claude_skills(source_root, generated)
        root = home / ".claude" / "skills"
        return {root / skill.name: (generated / skill.name).resolve() for skill in skills}
    raise ValueError(f"未知目标：{target}")


def install(
    source_root: Path,
    home: Path,
    *,
    target: str,
    repair_links: bool = False,
) -> list[str]:
    selected = ("codex", "claude") if target == "all" else (target,)
    results: list[str] = []
    for platform in selected:
        for link, destination in desired_targets(
            source_root, home, platform, prepare_claude=True
        ).items():
            status = ensure_link(link, destination, repair_links=repair_links)
            results.append(f"{platform}: {status}: {link} -> {destination}")
    return results


def _read_frontmatter_name(skill_path: Path) -> str | None:
    try:
        lines = skill_path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return None
    if not lines or lines[0].strip() != "---":
        return None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


def _skill_files_under(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    files: list[Path] = []
    for child in root.iterdir():
        direct = child / "SKILL.md"
        if direct.is_file():
            files.append(direct)
        if not child.is_dir() or _is_link_like(child):
            continue
        for current, dirs, names in os.walk(child, followlinks=False):
            current_path = Path(current)
            if current_path == child:
                pass
            dirs[:] = [
                name
                for name in dirs
                if name not in {
                    ".git", ".generated", "agents", "assets", "references",
                    "scripts", "__pycache__", "node_modules",
                }
            ]
            nested = current_path / "SKILL.md"
            if nested != direct and "SKILL.md" in names:
                files.append(nested)
    return sorted(set(files))


def _duplicate_errors(roots: list[Path], expected: set[str]) -> list[str]:
    by_name: dict[str, list[Path]] = {}
    for root in roots:
        for skill_path in _skill_files_under(root):
            name = _read_frontmatter_name(skill_path)
            if name in expected:
                by_name.setdefault(name, []).append(skill_path)
    return [
        f"发现重复 Skill {name}：" + "；".join(str(path) for path in paths)
        for name, paths in sorted(by_name.items())
        if len(paths) > 1
    ]


def check_install(
    source_root: Path,
    home: Path,
    *,
    target: str,
    project_root: Path | None = None,
) -> list[str]:
    selected = ("codex", "claude") if target == "all" else (target,)
    errors: list[str] = []
    expected = {skill.name for skill in discover_skill_dirs(source_root)}

    for platform in selected:
        for link, destination in desired_targets(
            source_root, home, platform, prepare_claude=False
        ).items():
            if not _same_target(link, destination):
                errors.append(f"{platform}: 映射缺失或目标错误：{link} -> {destination}")
                continue
            if platform == "claude":
                skill_path = destination / "SKILL.md"
                if not skill_path.is_file():
                    errors.append(f"claude: 缺少生成的 SKILL.md：{skill_path}")
                    continue
                parts = skill_path.read_text(encoding="utf-8").split("---", 2)
                frontmatter = parts[1] if len(parts) == 3 else ""
                has_explicit = "disable-model-invocation: true" in frontmatter
                expected_explicit = destination.name.startswith("siyk-")
                if has_explicit != expected_explicit:
                    errors.append(f"claude: 调用策略错误：{skill_path}")

    # 同一个 Skill 同时安装给 Codex 和 Claude 是正常的；只在单个宿主的
    # 发现范围内检查重复，不把两个客户端之间的同名包视为冲突。
    if "codex" in selected:
        errors.extend(_duplicate_errors([home / ".agents" / "skills"], expected))

    if "claude" in selected:
        claude_roots = [home / ".claude" / "skills"]
        commands_root = home / ".claude" / "commands"
        if commands_root.is_dir():
            for command in commands_root.rglob("*.md"):
                if command.stem in expected:
                    errors.append(f"Claude Code 旧 command 可能重复 /{command.stem}：{command}")
        if project_root is not None:
            project_root = project_root.resolve()
            claude_roots.append(project_root / ".claude" / "skills")
            project_commands = project_root / ".claude" / "commands"
            if project_commands.is_dir():
                for command in project_commands.rglob("*.md"):
                    if command.stem in expected:
                        errors.append(
                            f"项目级 Claude command 可能重复 /{command.stem}：{command}"
                        )
        errors.extend(_duplicate_errors(claude_roots, expected))

    return errors


def uninstall(source_root: Path, home: Path, *, target: str) -> list[str]:
    selected = ("codex", "claude") if target == "all" else (target,)
    results: list[str] = []
    names = [skill.name for skill in discover_skill_dirs(source_root)]
    for platform in selected:
        host_root = (home / ".agents" / "skills") if platform == "codex" else (home / ".claude" / "skills")
        for name in names:
            link = host_root / name
            if not _lexists(link):
                continue
            if _is_link_like(link) and _is_within(link.resolve(), source_root):
                _remove_link_only(link)
                results.append(f"{platform}: removed: {link}")
            else:
                results.append(f"{platform}: kept unmanaged path: {link}")
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--target", choices=("all", "codex", "claude"), default="all")
    parser.add_argument("--repair-links", action="store_true", help="只替换错误的 symlink/Junction")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="验证安装映射与重复来源")
    mode.add_argument("--uninstall", action="store_true", help="只移除指向当前 Collection 的链接")
    parser.add_argument(
        "--project-root",
        type=Path,
        help="检查项目级 .claude/skills 与 .claude/commands 的同名重复来源",
    )
    parser.add_argument(
        "--build-claude",
        type=Path,
        metavar="DIR",
        help="只在指定目录生成 Claude Code 变体，不创建安装链接",
    )
    args = parser.parse_args()

    try:
        if args.build_claude:
            built = build_claude_skills(args.root, args.build_claude)
            for path in built:
                print(path)
            return 0

        ensure_neutral_source(args.root, args.home)

        if args.uninstall:
            for result in uninstall(args.root, args.home, target=args.target):
                print(result)
            return 0

        if args.check:
            errors = check_install(
                args.root,
                args.home,
                target=args.target,
                project_root=args.project_root,
            )
            if errors:
                for error in errors:
                    print(f"错误：{error}", file=sys.stderr)
                return 1
            print("Codex / Claude Code Skill 安装映射与重复来源检查通过")
            return 0

        for result in install(
            args.root,
            args.home,
            target=args.target,
            repair_links=args.repair_links,
        ):
            print(result)
        print("安装完成；请在 Codex / Claude Code 新会话中验证 9 个平级 Skill。")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
