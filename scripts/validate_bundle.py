#!/usr/bin/env python3
"""Validate deterministic structure and release contract of siyrs-skill."""
from __future__ import annotations
import argparse, json, re
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
]
COMMANDS = ("/siyk-test-full", "/siyk-test-new", "/siyk-git-commit", "/siyk-git-sync")
IGNORED_PARTS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}

def actual_files(root: Path) -> list[str]:
    result=[]
    for path in root.rglob("*"):
        if not path.is_file(): continue
        rel=path.relative_to(root)
        if any(part in IGNORED_PARTS for part in rel.parts): continue
        if path.suffix in IGNORED_SUFFIXES or path.name==".DS_Store": continue
        result.append(rel.as_posix())
    return sorted(result)

def read_json(path: Path, errors: list[str]):
    try: data=json.loads(path.read_text(encoding="utf-8"))
    except (OSError,json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON {path.name}: {exc}"); return None
    if not isinstance(data,dict): errors.append(f"JSON root must be an object: {path.name}"); return None
    return data

def extract_version(text, pattern):
    m=re.search(pattern,text,flags=re.M); return m.group(1) if m else None

def validate(root: Path) -> dict:
    root=root.resolve(); errors=[]; warnings=[]
    skills=[p for p in root.rglob("*") if p.is_file() and p.name.lower()=="skill.md" and not any(x in IGNORED_PARTS for x in p.relative_to(root).parts)]
    if len(skills)!=1: errors.append(f"expected exactly one SKILL.md, found {len(skills)}")
    for rel in REQUIRED:
        if not (root/rel).is_file(): errors.append(f"missing required file: {rel}")
    version=(root/"VERSION").read_text(encoding="utf-8").strip() if (root/"VERSION").is_file() else None
    if version and not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?",version): errors.append(f"invalid VERSION value: {version!r}")
    if (root/"SKILL.md").is_file():
        text=(root/"SKILL.md").read_text(encoding="utf-8")
        fm=re.match(r"^---\r?\n(.*?)\r?\n---\r?\n",text,flags=re.S)
        if not fm: errors.append("SKILL.md frontmatter missing or malformed")
        else:
            block=fm.group(1)
            if not re.search(r"^name:\s*siyrs-skill\s*$",block,flags=re.M): errors.append("frontmatter name must be siyrs-skill")
            if not re.search(r"^description:\s*\S",block,flags=re.M): errors.append("frontmatter description is required")
        for command in COMMANDS:
            if command not in text: errors.append(f"manifest does not declare {command}")
        if version and extract_version(text,r"^Version:\s*\*\*(\S+)\*\*\s*$")!=version: errors.append("SKILL.md version does not match VERSION")
    if version and (root/"README.md").is_file():
        if extract_version((root/"README.md").read_text(encoding="utf-8"),r"当前版本：`v([^`]+)`")!=version: errors.append("README version does not match VERSION")
    if version and (root/"CHANGELOG.md").is_file():
        if extract_version((root/"CHANGELOG.md").read_text(encoding="utf-8"),r"^##\s+([0-9][^\s]*)\s+-\s+")!=version: errors.append("CHANGELOG latest version does not match VERSION")
    manifest=read_json(root/"release-manifest.json",errors) if (root/"release-manifest.json").is_file() else None
    if manifest is not None:
        if manifest.get("version")!=version: errors.append("release-manifest version does not match VERSION")
        declared=manifest.get("files")
        if not isinstance(declared,list) or not all(isinstance(x,str) for x in declared): errors.append("release-manifest files must be a string array")
        else:
            ds=sorted(set(declared)); actual=actual_files(root)
            if len(ds)!=len(declared): errors.append("release-manifest files contains duplicates or is not unique")
            a,b=sorted(set(actual)-set(ds)),sorted(set(ds)-set(actual))
            if a: errors.append(f"release-manifest omits files: {a}")
            if b: errors.append(f"release-manifest references missing files: {b}")
    for rel in ("schemas/config.schema.json","schemas/state.schema.json"):
        if (root/rel).is_file():
            schema=read_json(root/rel,errors)
            if schema and schema.get("$schema")!="https://json-schema.org/draft/2020-12/schema": warnings.append(f"{rel} does not declare JSON Schema 2020-12")
    if (root/"assets/state.example.json").is_file():
        state=read_json(root/"assets/state.example.json",errors)
        if state and state.get("version")!=1: errors.append("assets/state.example.json version must be 1")
    for command in COMMANDS:
        adapter=root/"adapters"/"claude-code"/"commands"/f"{command[1:]}.md"
        if not adapter.is_file(): errors.append(f"missing Claude Code adapter: {adapter.relative_to(root).as_posix()}")
        elif command not in adapter.read_text(encoding="utf-8") or "$ARGUMENTS" not in adapter.read_text(encoding="utf-8"): errors.append(f"invalid Claude Code adapter contract: {adapter.relative_to(root).as_posix()}")
    return {"root":str(root),"version":version,"valid":not errors,"files":len(actual_files(root)),"errors":errors,"warnings":warnings}

def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",default="."); a=p.parse_args(); r=validate(Path(a.root)); print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r["valid"] else 1
if __name__=="__main__": raise SystemExit(main())
