#!/usr/bin/env python3
"""Validate siyrs-skill structure, registry, schemas, adapters, CI, and release contract."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from command_registry import load_registry, parse_frontmatter
from config_model import load_config
from state import default_state

IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
REQUIRED_STATIC = {
    "VERSION", "SKILL.md", "README.md", "CHANGELOG.md", "release-manifest.json",
    "references/testing-common.md", "references/testing-tiers.md", "references/testing-selectors.md",
    "references/config-and-plans.md", "references/state-lifecycle.md", "references/git-content-scan.md",
    "references/output-contract.md", "scripts/command_registry.py", "scripts/config_model.py",
    "scripts/test_plan.py", "scripts/git_audit.py", "scripts/state.py", "scripts/route_command.py",
    "scripts/siyk.py", "schemas/config.schema.json", "schemas/state.schema.json",
    "assets/config.example.yaml", "assets/state.example.json", ".github/workflows/ci.yml",
    "adapters/claude-code/install.sh", "adapters/claude-code/install.ps1",
    "adapters/codex/install.sh", "adapters/codex/install.ps1", "docs/RELEASE-REPORT-v0.2.3.md",
}


def actual_files(root: Path) -> list[str]:
    result: list[str] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        if path.suffix in IGNORED_SUFFIXES or path.name == ".DS_Store":
            continue
        result.append(rel.as_posix())
    return sorted(result)


def read_json(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"JSON root must be object: {path}")
        return None
    return data


def version_from(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.M)
    return match.group(1) if match else None


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []
    for rel in sorted(REQUIRED_STATIC):
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else None
    if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        errors.append(f"invalid VERSION: {version!r}")

    try:
        specs = load_registry(root)
    except (OSError, ValueError) as exc:
        errors.append(f"invalid command registry: {exc}")
        specs = []
    commands = [spec.command for spec in specs]
    names = [spec.name for spec in specs if spec.client_entrypoint]
    legacy = sorted({item for spec in specs for item in spec.legacy_commands})
    if len(specs) != 6:
        errors.append(f"expected six commands, found {len(specs)}")

    skill_text = (root / "SKILL.md").read_text(encoding="utf-8") if (root / "SKILL.md").is_file() else ""
    try:
        frontmatter, _ = parse_frontmatter(root / "SKILL.md", {"name", "description"})
        if frontmatter.get("name") != "siyrs-skill":
            errors.append("root frontmatter name must be siyrs-skill")
    except (OSError, ValueError) as exc:
        errors.append(str(exc))
    for command in commands:
        if command not in skill_text:
            errors.append(f"root SKILL.md omits {command}")
    if version and version_from(skill_text, r"^Version:\s*\*\*(\S+)\*\*\s*$") != version:
        errors.append("SKILL.md version drift")

    readme = (root / "README.md").read_text(encoding="utf-8") if (root / "README.md").is_file() else ""
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8") if (root / "CHANGELOG.md").is_file() else ""
    if version and version_from(readme, r"当前版本：`v([^`]+)`") != version:
        errors.append("README version drift")
    if version and version_from(changelog, r"^##\s+([0-9][^\s]*)\s+-\s+") != version:
        errors.append("CHANGELOG version drift")

    manifest = read_json(root / "release-manifest.json", errors) if (root / "release-manifest.json").is_file() else None
    if manifest:
        if manifest.get("version") != version:
            errors.append("release-manifest version drift")
        if manifest.get("commands") != commands:
            errors.append("release-manifest commands differ from Markdown registry")
        declared = manifest.get("files")
        if not isinstance(declared, list) or not all(isinstance(item, str) for item in declared):
            errors.append("release-manifest files must be string array")
        else:
            actual = actual_files(root)
            if len(declared) != len(set(declared)):
                errors.append("release-manifest files duplicate")
            omitted = sorted(set(actual) - set(declared))
            missing = sorted(set(declared) - set(actual))
            if omitted:
                errors.append(f"release-manifest omits files: {omitted}")
            if missing:
                errors.append(f"release-manifest references missing files: {missing}")

    # Adapters exact and generated from registry.
    claude_dir = root / "adapters" / "claude-code" / "commands"
    claude = {path.stem for path in claude_dir.glob("*.md")} if claude_dir.is_dir() else set()
    if claude != set(names):
        errors.append(f"Claude adapter set mismatch: {sorted(claude)} != {sorted(names)}")
    codex_root = root / "adapters" / "codex" / "entrypoints"
    codex = {path.name for path in codex_root.iterdir() if path.is_dir()} if codex_root.is_dir() else set()
    if codex != set(names):
        errors.append(f"Codex entrypoint set mismatch: {sorted(codex)} != {sorted(names)}")
    for name in names:
        claude_file = claude_dir / f"{name}.md"
        if claude_file.is_file():
            text = claude_file.read_text(encoding="utf-8")
            if f"/{name}" not in text or "$ARGUMENTS" not in text or "siyrs-skill-command-adapter: true" not in text:
                errors.append(f"invalid Claude adapter: {name}")
        template = codex_root / name / "SKILL.template.md"
        metadata = codex_root / name / "agents" / "openai.yaml"
        if not template.is_file() or not metadata.is_file():
            errors.append(f"missing Codex entrypoint: {name}")

    # State schema must use explicit record definitions, not the broken baseRecord/allOf extension pattern.
    state_schema = read_json(root / "schemas/state.schema.json", errors)
    if state_schema:
        defs = state_schema.get("$defs", {})
        for record in ("authoringRecord", "t1Record", "t2Record", "t3Record"):
            value = defs.get(record, {})
            if "allOf" in value:
                errors.append(f"state schema {record} must not use allOf extension with closed base properties")
            if value.get("additionalProperties") is not False:
                errors.append(f"state schema {record} must explicitly close additional properties")
        if defs.get("t1Record", {}).get("properties", {}).get("promotion") is None:
            errors.append("state schema missing T1 promotion contract")

    state_example = read_json(root / "assets/state.example.json", errors)
    if state_example and state_example != default_state():
        errors.append("state example differs from state.py default_state")

    config_result = load_config(root, root / "assets" / "config.example.yaml", required=True)
    if not config_result["valid"]:
        errors.extend(f"config example: {message}" for message in config_result["errors"])

    # Portable Bash contracts and macOS CI.
    ci = (root / ".github/workflows/ci.yml").read_text(encoding="utf-8") if (root / ".github/workflows/ci.yml").is_file() else ""
    if "macos-latest" not in ci:
        errors.append("CI must include macos-latest adapter coverage")
    for rel in ("adapters/claude-code/install.sh", "adapters/codex/install.sh"):
        text = (root / rel).read_text(encoding="utf-8") if (root / rel).is_file() else ""
        if "mapfile" in text:
            errors.append(f"macOS-incompatible mapfile remains in {rel}")
        if "-mindepth" in text or "-maxdepth" in text:
            errors.append(f"GNU-only find depth option remains in {rel}")
        if "command_registry.py" not in text:
            errors.append(f"installer does not consume registry: {rel}")

    route_text = (root / "scripts" / "route_command.py").read_text(encoding="utf-8")
    if "check-ref-format" not in route_text or "--branch" not in route_text:
        errors.append("git-sync explicit branch validation is missing")
    if "audit --root" not in (root / "commands" / "git-commit.md").read_text(encoding="utf-8"):
        errors.append("git-commit does not invoke deterministic Git audit")
    if "promote-t1" not in (root / "commands" / "git-commit.md").read_text(encoding="utf-8"):
        errors.append("git-commit does not promote T1 evidence")

    return {
        "root": str(root),
        "version": version,
        "valid": not errors,
        "commands": commands,
        "legacy_commands": legacy,
        "files": len(actual_files(root)),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    result = validate(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
