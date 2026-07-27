#!/usr/bin/env python3
"""Validate the deterministic structure and release contract of siyrs-skill."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    "VERSION",
    "SKILL.md",
    "README.md",
    "CHANGELOG.md",
    "commands/test-full.md",
    "commands/test-new.md",
    "commands/git-commit.md",
    "commands/git-sync.md",
    "references/project-detection.md",
    "references/output-contract.md",
    "scripts/detect_project.py",
    "scripts/collect_git_changes.py",
    "scripts/fingerprint.py",
    "scripts/route_command.py",
    "scripts/scan_secrets.py",
    "scripts/state.py",
    "schemas/config.schema.json",
    "schemas/state.schema.json",
    ".github/workflows/ci.yml",
    "release-manifest.json",
]
COMMANDS = ("/siyk-test-full", "/siyk-test-new", "/siyk-git-commit", "/siyk-git-sync")
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def actual_files(root: Path) -> list[str]:
    result = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in IGNORED_PARTS for part in rel.parts):
            continue
        if path.suffix in IGNORED_SUFFIXES or path.name in {".DS_Store"}:
            continue
        result.append(rel.as_posix())
    return sorted(result)


def read_json(path: Path, errors: list[str]) -> dict | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.name}: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"JSON root must be an object: {path.name}")
        return None
    return data


def extract_version(text: str, pattern: str) -> str | None:
    match = re.search(pattern, text, flags=re.M)
    return match.group(1) if match else None


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skill_files = [
        p for p in root.rglob("*")
        if p.is_file() and p.name.lower() == "skill.md" and not any(part in IGNORED_PARTS for part in p.relative_to(root).parts)
    ]
    if len(skill_files) != 1:
        errors.append(f"expected exactly one SKILL.md, found {len(skill_files)}")

    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    version = None
    version_path = root / "VERSION"
    if version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
            errors.append(f"invalid VERSION value: {version!r}")

    manifest_path = root / "SKILL.md"
    if manifest_path.is_file():
        text = manifest_path.read_text(encoding="utf-8")
        fm = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.S)
        if not fm:
            errors.append("SKILL.md frontmatter missing or malformed")
        else:
            block = fm.group(1)
            if not re.search(r"^name:\s*siyrs-skill\s*$", block, flags=re.M):
                errors.append("frontmatter name must be siyrs-skill")
            if not re.search(r"^description:\s*\S", block, flags=re.M):
                errors.append("frontmatter description is required")
        for command in COMMANDS:
            if command not in text:
                errors.append(f"manifest does not declare {command}")
        skill_version = extract_version(text, r"^Version:\s*\*\*(\S+)\*\*\s*$")
        if version and skill_version != version:
            errors.append(f"SKILL.md version {skill_version!r} does not match VERSION {version!r}")

    readme_path = root / "README.md"
    if readme_path.is_file() and version:
        readme = readme_path.read_text(encoding="utf-8")
        readme_version = extract_version(readme, r"当前版本：`v([^`]+)`")
        if readme_version != version:
            errors.append(f"README version {readme_version!r} does not match VERSION {version!r}")

    changelog_path = root / "CHANGELOG.md"
    if changelog_path.is_file() and version:
        changelog = changelog_path.read_text(encoding="utf-8")
        latest = extract_version(changelog, r"^##\s+([0-9][^\s]*)\s+-\s+")
        if latest != version:
            errors.append(f"CHANGELOG latest version {latest!r} does not match VERSION {version!r}")

    release_manifest = read_json(root / "release-manifest.json", errors) if (root / "release-manifest.json").is_file() else None
    if release_manifest is not None:
        if version and release_manifest.get("version") != version:
            errors.append("release-manifest version does not match VERSION")
        declared = release_manifest.get("files")
        if not isinstance(declared, list) or not all(isinstance(item, str) for item in declared):
            errors.append("release-manifest files must be a string array")
        else:
            declared_sorted = sorted(set(declared))
            if len(declared_sorted) != len(declared):
                errors.append("release-manifest files contains duplicates or is not unique")
            actual = actual_files(root)
            missing_from_manifest = sorted(set(actual) - set(declared_sorted))
            missing_from_bundle = sorted(set(declared_sorted) - set(actual))
            if missing_from_manifest:
                errors.append(f"release-manifest omits files: {missing_from_manifest}")
            if missing_from_bundle:
                errors.append(f"release-manifest references missing files: {missing_from_bundle}")

    for schema_rel in ("schemas/config.schema.json", "schemas/state.schema.json"):
        schema_path = root / schema_rel
        if schema_path.is_file():
            schema = read_json(schema_path, errors)
            if schema and schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                warnings.append(f"{schema_rel} does not declare JSON Schema 2020-12")

    state_example = root / "assets/state.example.json"
    if state_example.is_file():
        state = read_json(state_example, errors)
        if state and state.get("version") != 1:
            errors.append("assets/state.example.json version must be 1")

    for command in COMMANDS:
        adapter = root / "adapters" / "claude-code" / "commands" / f"{command[1:]}.md"
        if not adapter.is_file():
            errors.append(f"missing Claude Code adapter: {adapter.relative_to(root).as_posix()}")
        else:
            adapter_text = adapter.read_text(encoding="utf-8")
            if command not in adapter_text or "$ARGUMENTS" not in adapter_text:
                errors.append(f"invalid Claude Code adapter contract: {adapter.relative_to(root).as_posix()}")

    return {
        "root": str(root),
        "version": version,
        "valid": not errors,
        "files": len(actual_files(root)),
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate siyrs-skill bundle")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    result = validate(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
