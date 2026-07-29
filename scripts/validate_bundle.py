#!/usr/bin/env python3
"""Validate deterministic structure and release contract of siyrs-skill."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

REQUIRED = [
    "VERSION", "SKILL.md", "README.md", "CHANGELOG.md",
    "commands/test-full.md", "commands/test-new.md", "commands/git-commit.md", "commands/git-sync.md",
    "references/project-detection.md", "references/testing-common.md", "references/git-policy.md",
    "references/git-content-scan.md", "references/risk-authorization.md", "references/subworkflow-composition.md",
    "references/safety-and-authorization.md", "references/output-contract.md",
    "scripts/detect_project.py", "scripts/collect_git_changes.py", "scripts/fingerprint.py",
    "scripts/route_command.py", "scripts/scan_secrets.py", "scripts/state.py",
    "schemas/config.schema.json", "schemas/state.schema.json", ".github/workflows/ci.yml", "release-manifest.json",
    "adapters/codex/README.md", "adapters/codex/install.sh", "adapters/codex/install.ps1",
]
COMMANDS = ("/siyk-test-full", "/siyk-test-new", "/siyk-git-commit", "/siyk-git-sync")
CODEX_NAMES = tuple(command[1:] for command in COMMANDS)
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


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


def read_json(path: Path, errors: list[str]):
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


def parse_frontmatter(text: str) -> str | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, flags=re.S)
    return match.group(1) if match else None


def validate(root: Path) -> dict:
    root = root.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    skill_files = [
        path for path in root.rglob("*")
        if path.is_file()
        and path.name.lower() == "skill.md"
        and not any(part in IGNORED_PARTS for part in path.relative_to(root).parts)
    ]
    if len(skill_files) != 1:
        errors.append(f"expected exactly one source SKILL.md, found {len(skill_files)}")

    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f"missing required file: {rel}")

    version = (root / "VERSION").read_text(encoding="utf-8").strip() if (root / "VERSION").is_file() else None
    if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?", version):
        errors.append(f"invalid VERSION value: {version!r}")

    if (root / "SKILL.md").is_file():
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            errors.append("SKILL.md frontmatter missing or malformed")
        else:
            if not re.search(r"^name:\s*siyrs-skill\s*$", frontmatter, flags=re.M):
                errors.append("frontmatter name must be siyrs-skill")
            if not re.search(r"^description:\s*\S", frontmatter, flags=re.M):
                errors.append("frontmatter description is required")
        for command in COMMANDS:
            if command not in text:
                errors.append(f"manifest does not declare {command}")
        if version and extract_version(text, r"^Version:\s*\*\*(\S+)\*\*\s*$") != version:
            errors.append("SKILL.md version does not match VERSION")

    if version and (root / "README.md").is_file():
        if extract_version((root / "README.md").read_text(encoding="utf-8"), r"当前版本：`v([^`]+)`") != version:
            errors.append("README version does not match VERSION")
    if version and (root / "CHANGELOG.md").is_file():
        if extract_version((root / "CHANGELOG.md").read_text(encoding="utf-8"), r"^##\s+([0-9][^\s]*)\s+-\s+") != version:
            errors.append("CHANGELOG latest version does not match VERSION")

    manifest = read_json(root / "release-manifest.json", errors) if (root / "release-manifest.json").is_file() else None
    if manifest is not None:
        if manifest.get("version") != version:
            errors.append("release-manifest version does not match VERSION")
        declared = manifest.get("files")
        if not isinstance(declared, list) or not all(isinstance(item, str) for item in declared):
            errors.append("release-manifest files must be a string array")
        else:
            declared_unique = sorted(set(declared))
            actual = actual_files(root)
            if len(declared_unique) != len(declared):
                errors.append("release-manifest files contains duplicates or is not unique")
            omitted = sorted(set(actual) - set(declared_unique))
            missing = sorted(set(declared_unique) - set(actual))
            if omitted:
                errors.append(f"release-manifest omits files: {omitted}")
            if missing:
                errors.append(f"release-manifest references missing files: {missing}")

    for rel in ("schemas/config.schema.json", "schemas/state.schema.json"):
        if (root / rel).is_file():
            schema = read_json(root / rel, errors)
            if schema and schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
                warnings.append(f"{rel} does not declare JSON Schema 2020-12")
    if (root / "assets/state.example.json").is_file():
        state = read_json(root / "assets/state.example.json", errors)
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

    codex_root = root / "adapters" / "codex" / "entrypoints"
    for name in CODEX_NAMES:
        template = codex_root / name / "SKILL.template.md"
        metadata = codex_root / name / "agents" / "openai.yaml"
        if not template.is_file():
            errors.append(f"missing Codex entrypoint template: {template.relative_to(root).as_posix()}")
            continue
        text = template.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)
        if frontmatter is None:
            errors.append(f"Codex entrypoint frontmatter missing: {name}")
        else:
            if not re.search(rf"^name:\s*{re.escape(name)}\s*$", frontmatter, flags=re.M):
                errors.append(f"Codex entrypoint name mismatch: {name}")
            if not re.search(r"^description:\s*\S", frontmatter, flags=re.M):
                errors.append(f"Codex entrypoint description missing: {name}")
        if "<skills-root>/siyrs-skill/SKILL.md" not in text or f"/{name}" not in text:
            errors.append(f"Codex entrypoint does not delegate to core: {name}")
        if not metadata.is_file():
            errors.append(f"missing Codex entrypoint metadata: {name}")
        else:
            metadata_text = metadata.read_text(encoding="utf-8")
            if f'display_name: "/{name}"' not in metadata_text:
                errors.append(f"Codex display name mismatch: {name}")
            if "allow_implicit_invocation: false" not in metadata_text:
                errors.append(f"Codex entrypoint must be explicit-only: {name}")

    return {
        "root": str(root),
        "version": version,
        "valid": not errors,
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
