#!/usr/bin/env python3
"""Deterministically detect common project/module types.

This script provides repository evidence for the agent. It does not replace source
inspection or framework-specific dependency review.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

EXCLUDED = {
    ".git", ".idea", ".vscode", "node_modules", "target", "build", "dist",
    "coverage", ".gradle", ".pytest_cache", "__pycache__", ".venv", "venv",
    ".mypy_cache", ".ruff_cache",
}
MAX_DEPTH = 5


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if any(part in EXCLUDED for part in rel.parts):
            continue
        if len(rel.parts) > MAX_DEPTH + 1:
            continue
        if path.is_file():
            yield path


def safe_package_dependencies(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    result: set[str] = set()
    for key in ("dependencies", "devDependencies", "peerDependencies"):
        values = data.get(key, {})
        if isinstance(values, dict):
            result.update(str(name).lower() for name in values)
    return result


def detect(root: Path) -> dict:
    root = root.resolve()
    paths = list(iter_files(root))
    rels = {path.relative_to(root).as_posix(): path for path in paths}
    evidence: dict[str, list[str]] = {}

    def add(kind: str, *items: str) -> None:
        values = [item for item in items if item]
        if values:
            evidence.setdefault(kind, []).extend(values)

    gradle_or_maven = sorted(
        rel for rel in rels
        if Path(rel).name in {"pom.xml", "build.gradle", "build.gradle.kts", "settings.gradle", "settings.gradle.kts"}
    )
    add("java_or_gradle", *gradle_or_maven)

    android_manifests = sorted(
        rel for rel in rels
        if rel.endswith("src/main/AndroidManifest.xml") or rel == "AndroidManifest.xml"
    )
    add("android", *android_manifests)

    package_files = sorted(rel for rel in rels if Path(rel).name == "package.json")
    add("javascript_typescript", *package_files)

    python_manifests = sorted(
        rel for rel in rels
        if Path(rel).name in {"pyproject.toml", "requirements.txt", "setup.py", "setup.cfg", "tox.ini", "Pipfile"}
        or Path(rel).name.startswith("requirements-")
    )
    add("python", *python_manifests)

    skill_manifests = sorted(rel for rel in rels if Path(rel).name.lower() == "skill.md")
    add("agent_skill", *skill_manifests)

    source_evidence = {
        "java": [rel for rel in rels if "/src/main/java/" in f"/{rel}" or rel.startswith("src/main/java/")][:20],
        "kotlin": [rel for rel in rels if "/src/main/kotlin/" in f"/{rel}" or rel.startswith("src/main/kotlin/")][:20],
        "android_test": [rel for rel in rels if "/src/androidTest/" in f"/{rel}"][:20],
        "frontend": [
            rel for rel in rels
            if any(segment in f"/{rel}" for segment in ("/src/pages/", "/src/components/", "/src/routes/", "/app/"))
            and Path(rel).suffix.lower() in {".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
        ][:20],
        "python": [rel for rel in rels if rel.endswith(".py")][:20],
    }
    for kind, items in source_evidence.items():
        add(f"source_{kind}", *items)

    js_dependencies: set[str] = set()
    for rel in package_files:
        js_dependencies.update(safe_package_dependencies(rels[rel]))
    frontend_dependencies = {
        "react", "vue", "@angular/core", "svelte", "next", "nuxt", "vite",
        "@vitejs/plugin-vue", "@vitejs/plugin-react",
    }
    node_backend_dependencies = {
        "express", "fastify", "koa", "@nestjs/core", "hapi", "adonisjs", "typeorm", "prisma",
    }
    if js_dependencies & frontend_dependencies:
        add("frontend_dependencies", *sorted(js_dependencies & frontend_dependencies))
    if js_dependencies & node_backend_dependencies:
        add("node_backend_dependencies", *sorted(js_dependencies & node_backend_dependencies))

    has_android = bool(android_manifests)
    has_java = bool(gradle_or_maven or source_evidence["java"] or source_evidence["kotlin"])
    has_js = bool(package_files)
    has_frontend = bool(source_evidence["frontend"] or js_dependencies & frontend_dependencies)
    has_node_backend = bool(js_dependencies & node_backend_dependencies)
    has_python = bool(python_manifests or source_evidence["python"])

    types: list[str] = []
    if has_android:
        types.append("android")
    elif has_java:
        types.append("java-backend-or-library")

    if has_js:
        if has_frontend and (has_node_backend or has_java or has_python):
            types.append("full-stack-web")
        elif has_frontend:
            types.append("web-frontend")
        elif has_node_backend:
            types.append("node-backend")
        else:
            types.append("node-or-js-project")

    if has_python:
        types.append("python")
    if skill_manifests:
        types.append("agent-skill")
    if not types:
        types.append("unknown-custom")

    manifest_dirs = {
        str(Path(rel).parent)
        for rel in gradle_or_maven + package_files + python_manifests
    }
    manifest_dirs.discard(".")
    if len(package_files) > 1 or len(manifest_dirs) > 1:
        types.append("possible-monorepo")

    strong_keys = {
        "android", "java_or_gradle", "javascript_typescript", "python", "agent_skill",
        "source_java", "source_kotlin", "source_python",
    }
    confidence = "high" if any(key in evidence for key in strong_keys) else "low"
    return {
        "root": str(root),
        "types": types,
        "confidence": confidence,
        "module_roots": sorted(manifest_dirs) or ["."],
        "evidence": {key: sorted(set(values)) for key, values in sorted(evidence.items())},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect common repository project types")
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")
    args = parser.parse_args()
    result = detect(Path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
