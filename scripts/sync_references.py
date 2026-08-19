#!/usr/bin/env python3
"""将共享 Markdown reference 确定性物化到每个独立 Agent Skill。"""

from __future__ import annotations

import argparse
import re
import sys
from collections import deque
from pathlib import Path

LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")


def discover_skill_dirs(root: Path) -> list[Path]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return []
    return sorted(
        (path for path in skills_root.iterdir() if (path / "SKILL.md").is_file()),
        key=lambda path: path.name,
    )


def _local_markdown_links(text: str) -> list[str]:
    links: list[str] = []
    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split("#", 1)[0].split("?", 1)[0]
        if not target or target.startswith(("http://", "https://", "mailto:", "#", "/")):
            continue
        if target.endswith(".md"):
            links.append(target)
    return links


def required_reference_paths(root: Path, skill_dir: Path) -> set[Path]:
    shared_root = (root / "shared" / "references").resolve()
    skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")

    queue: deque[Path] = deque()
    for target in _local_markdown_links(skill_text):
        if target.startswith("references/"):
            queue.append(Path(target).relative_to("references"))

    required: set[Path] = set()
    while queue:
        rel = queue.popleft()
        if rel in required:
            continue
        source = (shared_root / rel).resolve()
        try:
            source.relative_to(shared_root)
        except ValueError as exc:
            raise ValueError(f"{skill_dir.name}: reference 越过 shared/references：{rel}") from exc
        if not source.is_file():
            raise FileNotFoundError(f"{skill_dir.name}: 缺少共享 reference：{rel}")

        required.add(rel)
        for target in _local_markdown_links(source.read_text(encoding="utf-8")):
            nested = (shared_root / rel.parent / target).resolve()
            try:
                nested_rel = nested.relative_to(shared_root)
            except ValueError as exc:
                raise ValueError(f"{rel}: reference 链接越过 shared/references：{target}") from exc
            if (shared_root / nested_rel).is_file():
                queue.append(nested_rel)

    return required


def reference_sync_errors(root: Path) -> list[str]:
    root = root.resolve()
    shared_root = root / "shared" / "references"
    errors: list[str] = []

    if not shared_root.is_dir():
        return [f"缺少共享 reference 目录：{shared_root}"]

    for skill_dir in discover_skill_dirs(root):
        try:
            required = required_reference_paths(root, skill_dir)
        except (FileNotFoundError, ValueError) as exc:
            errors.append(str(exc))
            continue

        refs_dir = skill_dir / "references"
        actual = {
            path.relative_to(refs_dir)
            for path in refs_dir.rglob("*.md")
        } if refs_dir.is_dir() else set()

        for rel in sorted(required - actual):
            errors.append(f"{skill_dir.name}: 缺少已物化 reference：references/{rel}")
        for rel in sorted(actual - required):
            errors.append(f"{skill_dir.name}: 存在未使用或过期 reference：references/{rel}")
        for rel in sorted(required & actual):
            source = shared_root / rel
            target = refs_dir / rel
            if source.read_bytes() != target.read_bytes():
                errors.append(f"{skill_dir.name}: reference 与共享源不一致：references/{rel}")

    return errors


def sync_references(root: Path) -> None:
    root = root.resolve()
    shared_root = root / "shared" / "references"
    for skill_dir in discover_skill_dirs(root):
        required = required_reference_paths(root, skill_dir)
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(parents=True, exist_ok=True)

        for rel in required:
            source = shared_root / rel
            target = refs_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())

        for path in sorted(refs_dir.rglob("*.md"), reverse=True):
            if path.relative_to(refs_dir) not in required:
                path.unlink()
        for path in sorted((p for p in refs_dir.rglob("*") if p.is_dir()), reverse=True):
            try:
                path.rmdir()
            except OSError:
                pass
        try:
            refs_dir.rmdir()
        except OSError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="只检查，不写入")
    args = parser.parse_args()

    if args.check:
        errors = reference_sync_errors(args.root)
        if errors:
            for error in errors:
                print(f"错误：{error}", file=sys.stderr)
            return 1
        print("共享 reference 物化检查通过")
        return 0

    sync_references(args.root)
    errors = reference_sync_errors(args.root)
    if errors:
        for error in errors:
            print(f"错误：{error}", file=sys.stderr)
        return 1
    print("共享 reference 已同步")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
