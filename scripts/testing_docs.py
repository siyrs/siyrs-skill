#!/usr/bin/env python3
"""Resolve, create, index, and validate the Markdown-first testing workspace.

Policy remains in references/testing-documentation.md. This helper only performs
safe path resolution and deterministic Markdown/document-contract checks.
"""
from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote

from command_registry import parse_frontmatter
from config_model import ConfigError, load_config

DEFAULT_ROOT = "docs/testing"
DEFAULT_INDEX = "README.md"
DEFAULT_EVIDENCE_ROOT = "evidence"
INDEX_START = "<!-- siyrs-testing-index:start -->"
INDEX_END = "<!-- siyrs-testing-index:end -->"
VALID_DOCUMENT_TYPES = {
    "index",
    "governance",
    "tiers",
    "shared-reference",
    "case-module",
    "cross-module",
    "evidence",
    "release-record",
    "inventory",
    "matrix",
    "uat-plan",
}
VALID_PLATFORMS = {
    "backend",
    "frontend",
    "full-stack",
    "android",
    "ios",
    "cli",
    "service",
    "data",
    "infrastructure",
    "custom",
}
TC_RE = re.compile(r"\bTC-[A-Z0-9][A-Z0-9-]*-\d{3,}\b")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)
TABLE_SEPARATOR_RE = re.compile(r"^:?-{3,}:?$")


@dataclass(frozen=True)
class Workspace:
    repository_root: str
    docs_root: str
    index: str
    entry: str
    evidence_root: str
    source: str
    config_path: str
    config_exists: bool
    agent_discovery: bool


@dataclass(frozen=True)
class Document:
    path: str
    title: str
    document_type: str
    module: str | None
    case_prefixes: tuple[str, ...]
    platforms: tuple[str, ...]
    indexed: bool
    metadata_present: bool


def _safe_relative(value: str, label: str) -> str:
    value = value.strip().replace("\\", "/")
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise ConfigError(f"{label} must be a safe repository-relative path: {value!r}")
    return path.as_posix()


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _existing_index_variant(docs_dir: Path, requested: str) -> str:
    if not docs_dir.is_dir():
        return requested
    matches = [path.name for path in docs_dir.iterdir() if path.is_file() and path.name.casefold() == requested.casefold()]
    if len(matches) == 1:
        return matches[0]
    if len(matches) > 1:
        raise ConfigError(f"case-insensitive testing index collision: {sorted(matches)}")
    return requested


def resolve_workspace(
    root: Path,
    *,
    docs_root: str | None = None,
    index: str | None = None,
    entry: str | None = None,
    config_path: Path | None = None,
) -> Workspace:
    root = root.resolve()
    loaded = load_config(root, config_path)
    config = loaded["config"]
    documentation = ((config.get("testing") or {}).get("documentation") or {})
    if not isinstance(documentation, dict):
        documentation = {}

    source = "default"
    root_value = str(documentation.get("root") or DEFAULT_ROOT)
    index_value = str(documentation.get("index") or DEFAULT_INDEX)
    evidence_value = str(documentation.get("evidence_root") or DEFAULT_EVIDENCE_ROOT)
    if loaded["exists"] and ("documentation" in ((config.get("testing") or {}))):
        source = "config"

    if entry:
        entry_value = _safe_relative(entry, "entry")
        entry_path = Path(entry_value)
        if entry_path.name in {"", "."}:
            raise ConfigError("entry must identify a Markdown file")
        root_value = entry_path.parent.as_posix() if entry_path.parent.as_posix() != "." else "."
        index_value = entry_path.name
        source = "user-entry"
    else:
        if docs_root:
            root_value = docs_root
            source = "user-root"
        if index:
            index_value = index
            source = "user-index" if source == "default" else source

    root_value = _safe_relative(root_value, "testing documentation root")
    index_value = _safe_relative(index_value, "testing documentation index")
    if len(Path(index_value).parts) != 1:
        raise ConfigError("testing documentation index must be a file name inside the documentation root")
    evidence_value = _safe_relative(evidence_value, "testing evidence root")

    docs_dir = (root / root_value).resolve()
    if not _inside(root, docs_dir):
        raise ConfigError("testing documentation root escapes repository")
    index_value = _existing_index_variant(docs_dir, index_value)
    entry_path = docs_dir / index_value
    evidence_path = docs_dir / evidence_value
    if not _inside(docs_dir, entry_path) or not _inside(docs_dir, evidence_path):
        raise ConfigError("testing documentation entry/evidence path escapes documentation root")

    return Workspace(
        repository_root=str(root),
        docs_root=Path(root_value).as_posix(),
        index=index_value,
        entry=(Path(root_value) / index_value).as_posix(),
        evidence_root=(Path(root_value) / evidence_value).as_posix(),
        source=source,
        config_path=loaded["path"],
        config_exists=bool(loaded["exists"]),
        agent_discovery=bool(documentation.get("agent_discovery", True)),
    )


def _metadata_list(value: Any) -> tuple[str, ...]:
    if isinstance(value, str):
        return (value,) if value else ()
    if isinstance(value, list):
        return tuple(str(item) for item in value if str(item).strip())
    return ()


def _infer_type(relative: Path, index_name: str) -> str:
    name = relative.name.casefold()
    parts = {part.casefold() for part in relative.parts}
    if relative.name.casefold() == index_name.casefold():
        return "index"
    if "evidence" in parts or "evidence" in name or "result" in name or "execution" in name:
        return "evidence"
    if name.startswith("00-") and "govern" in name:
        return "governance"
    if name.startswith("00-") and ("tier" in name or "level" in name):
        return "tiers"
    if name.startswith("_shared-") or name.startswith("shared-"):
        return "shared-reference"
    if name.startswith("99-") or "cross-module" in name:
        return "cross-module"
    if "matrix" in name:
        return "matrix"
    if "inventory" in name:
        return "inventory"
    if "uat" in name and "evidence" not in name:
        return "uat-plan"
    return "case-module"


def _first_heading(text: str, fallback: str) -> str:
    match = HEADING_RE.search(text)
    return match.group(1).strip() if match else fallback


def read_document(path: Path, docs_dir: Path, index_name: str) -> Document:
    text = path.read_text(encoding="utf-8")
    metadata: dict[str, Any] = {}
    metadata_present = False
    try:
        metadata, _ = parse_frontmatter(path, set())
        metadata_present = bool(metadata)
    except ValueError:
        metadata = {}
    relative = path.relative_to(docs_dir)
    inferred = _infer_type(relative, index_name)
    document_type = str(metadata.get("document_type") or inferred)
    module = metadata.get("module")
    module_value = str(module).strip() if module not in (None, "") else None
    prefixes = _metadata_list(metadata.get("case_prefixes"))
    platforms = tuple(item.casefold() for item in _metadata_list(metadata.get("platforms")))
    indexed = metadata.get("indexed", True) is not False
    return Document(
        path=relative.as_posix(),
        title=str(metadata.get("title") or _first_heading(text, relative.stem)),
        document_type=document_type,
        module=module_value,
        case_prefixes=prefixes,
        platforms=platforms,
        indexed=indexed,
        metadata_present=metadata_present,
    )


def scan_documents(workspace: Workspace) -> list[Document]:
    root = Path(workspace.repository_root)
    docs_dir = root / workspace.docs_root
    if not docs_dir.is_dir():
        return []
    documents = [
        read_document(path, docs_dir, workspace.index)
        for path in sorted(docs_dir.rglob("*.md"), key=lambda item: item.as_posix().casefold())
        if path.is_file()
    ]
    return documents


def _template_root() -> Path:
    return Path(__file__).resolve().parents[1] / "assets" / "templates"


def _copy_template(template_name: str, target: Path, replacements: dict[str, str]) -> bool:
    if target.exists():
        return False
    template = _template_root() / template_name
    text = template.read_text(encoding="utf-8")
    for key, value in replacements.items():
        text = text.replace(f"{{{{{key}}}}}", value)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    return True


def ensure_workspace(
    root: Path,
    *,
    docs_root: str | None = None,
    index: str | None = None,
    entry: str | None = None,
    config_path: Path | None = None,
) -> dict[str, Any]:
    workspace = resolve_workspace(root, docs_root=docs_root, index=index, entry=entry, config_path=config_path)
    repository = Path(workspace.repository_root)
    docs_dir = repository / workspace.docs_root
    evidence_dir = repository / workspace.evidence_root
    docs_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir.mkdir(parents=True, exist_ok=True)
    project_name = repository.name
    replacements = {
        "PROJECT_NAME": project_name,
        "INDEX_NAME": workspace.index,
        "EVIDENCE_ROOT": Path(workspace.evidence_root).relative_to(Path(workspace.docs_root)).as_posix(),
    }
    created: list[str] = []
    targets = [
        ("TESTING-README.template.md", docs_dir / workspace.index),
        ("TEST-GOVERNANCE.template.md", docs_dir / "00-test-governance.md"),
        ("TEST-TIERS.template.md", docs_dir / "00-test-tiers.md"),
    ]
    for template, target in targets:
        if _copy_template(template, target, replacements):
            created.append(target.relative_to(repository).as_posix())
    index_result = index_workspace(
        repository,
        docs_root=workspace.docs_root,
        index=workspace.index,
        config_path=config_path,
    )
    return {
        "workspace": asdict(workspace),
        "created": created,
        "index_updated": index_result["updated"],
        "documents": index_result["documents"],
    }


def _escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ")


def _index_block(documents: list[Document]) -> str:
    rows = [
        INDEX_START,
        "| Document | Type | Module | Case prefixes | Platforms |",
        "|---|---|---|---|---|",
    ]
    for doc in documents:
        if doc.document_type == "index" or not doc.indexed:
            continue
        label = _escape_table(doc.title)
        link = doc.path.replace(" ", "%20")
        rows.append(
            "| "
            + f"[{label}](./{link}) | {_escape_table(doc.document_type)} | "
            + f"{_escape_table(doc.module or '—')} | {_escape_table(', '.join(doc.case_prefixes) or '—')} | "
            + f"{_escape_table(', '.join(doc.platforms) or '—')} |"
        )
    rows.append(INDEX_END)
    return "\n".join(rows)


def index_workspace(
    root: Path,
    *,
    docs_root: str | None = None,
    index: str | None = None,
    entry: str | None = None,
    config_path: Path | None = None,
) -> dict[str, Any]:
    workspace = resolve_workspace(root, docs_root=docs_root, index=index, entry=entry, config_path=config_path)
    repository = Path(workspace.repository_root)
    docs_dir = repository / workspace.docs_root
    index_path = repository / workspace.entry
    if not index_path.is_file():
        raise ConfigError(f"testing documentation index does not exist: {workspace.entry}")
    documents = scan_documents(workspace)
    block = _index_block(documents)
    text = index_path.read_text(encoding="utf-8")
    if INDEX_START in text and INDEX_END in text:
        start = text.index(INDEX_START)
        end = text.index(INDEX_END, start) + len(INDEX_END)
        updated_text = text[:start] + block + text[end:]
    else:
        separator = "" if text.endswith("\n\n") else ("\n" if text.endswith("\n") else "\n\n")
        updated_text = text + separator + "## Managed test document index\n\n" + block + "\n"
    updated = updated_text != text
    if updated:
        index_path.write_text(updated_text, encoding="utf-8", newline="\n")
    return {
        "workspace": asdict(workspace),
        "updated": updated,
        "documents": [asdict(document) for document in documents],
    }


def _split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return []
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _tables(text: str) -> Iterable[tuple[list[str], list[list[str]]]]:
    lines = text.splitlines()
    index = 0
    while index + 1 < len(lines):
        header = _split_table_row(lines[index])
        separator = _split_table_row(lines[index + 1])
        if header and len(separator) == len(header) and all(TABLE_SEPARATOR_RE.fullmatch(cell.replace(" ", "")) for cell in separator):
            rows: list[list[str]] = []
            index += 2
            while index < len(lines):
                row = _split_table_row(lines[index])
                if not row or len(row) != len(header):
                    break
                rows.append(row)
                index += 1
            yield header, rows
            continue
        index += 1


def _header_index(headers: list[str], candidates: set[str]) -> int | None:
    normalized = [re.sub(r"[\s_/-]+", "", item).casefold() for item in headers]
    candidate_norm = {re.sub(r"[\s_/-]+", "", item).casefold() for item in candidates}
    for index, value in enumerate(normalized):
        if value in candidate_norm:
            return index
    return None


def _case_rows(document: Document, text: str) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for headers, rows in _tables(text):
        case_index = _header_index(headers, {"用例编号", "用例ID", "Case ID", "Case IDs", "Test Case ID", "编号"})
        if case_index is None:
            continue
        tier_index = _header_index(headers, {"档位", "Tier"})
        role_index = _header_index(headers, {"角色", "Role", "用例角色", "类型"})
        module_index = _header_index(headers, {"模块", "Module"})
        evidence_like = any(
            _header_index(headers, {candidate}) is not None
            for candidate in ("执行结果", "Result", "证据", "Evidence", "环境", "Environment", "Run ID")
        )
        definition_table = document.document_type in {"case-module", "cross-module"} and not evidence_like
        for row in rows:
            case_ids = TC_RE.findall(row[case_index])
            for case_id in case_ids:
                result.append({
                    "case_id": case_id,
                    "definition": definition_table,
                    "tier": row[tier_index].strip() if tier_index is not None else "",
                    "role": row[role_index].strip() if role_index is not None else "",
                    "module": row[module_index].strip() if module_index is not None else (document.module or document.path),
                })
    return result


def _readme_links(index_path: Path, docs_dir: Path) -> set[str]:
    text = index_path.read_text(encoding="utf-8")
    links: set[str] = set()
    for raw in LINK_RE.findall(text):
        target = _link_target(raw)
        if target is None:
            continue
        resolved = (index_path.parent / target).resolve()
        if _inside(docs_dir, resolved) and resolved.is_file():
            links.add(resolved.relative_to(docs_dir).as_posix())
    return links


def _link_target(raw: str) -> str | None:
    raw = raw.strip().strip("<>")
    if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "data:")):
        return None
    value = unquote(raw.split("#", 1)[0].split("?", 1)[0])
    return value or None


def validate_workspace(
    root: Path,
    *,
    docs_root: str | None = None,
    index: str | None = None,
    entry: str | None = None,
    config_path: Path | None = None,
    strict: bool = False,
) -> dict[str, Any]:
    workspace = resolve_workspace(root, docs_root=docs_root, index=index, entry=entry, config_path=config_path)
    repository = Path(workspace.repository_root)
    docs_dir = repository / workspace.docs_root
    index_path = repository / workspace.entry
    errors: list[str] = []
    warnings: list[str] = []
    debts: list[str] = []

    if not docs_dir.is_dir():
        errors.append(f"testing documentation root does not exist: {workspace.docs_root}")
        return {"valid": False, "workspace": asdict(workspace), "errors": errors, "warnings": warnings, "debts": debts, "documents": []}

    index_variants = [path.name for path in docs_dir.iterdir() if path.is_file() and path.name.casefold() == workspace.index.casefold()]
    if len(index_variants) > 1:
        errors.append(f"case-insensitive index collision: {sorted(index_variants)}")
    if not index_path.is_file():
        errors.append(f"testing documentation index does not exist: {workspace.entry}")

    documents = scan_documents(workspace)
    by_path = {document.path: document for document in documents}
    for document in documents:
        if document.document_type not in VALID_DOCUMENT_TYPES:
            errors.append(f"invalid document_type {document.document_type!r}: {document.path}")
        invalid_platforms = sorted(set(document.platforms) - VALID_PLATFORMS)
        if invalid_platforms:
            errors.append(f"invalid platforms in {document.path}: {invalid_platforms}")
        if not document.metadata_present:
            warnings.append(f"legacy document has no siyrs testing frontmatter: {document.path}")

    linked_from_index: set[str] = set()
    if index_path.is_file():
        index_text = index_path.read_text(encoding="utf-8")
        if workspace.agent_discovery and "Agent discovery" not in index_text and "智能体发现" not in index_text:
            debts.append("testing index does not declare the agent discovery contract")
        linked_from_index = _readme_links(index_path, docs_dir)

    for document in documents:
        path = docs_dir / document.path
        text = path.read_text(encoding="utf-8")
        for raw_link in LINK_RE.findall(text):
            target = _link_target(raw_link)
            if target is None:
                continue
            resolved = (path.parent / target).resolve()
            if not _inside(docs_dir, resolved):
                warnings.append(f"link leaves testing workspace: {document.path} -> {raw_link}")
                continue
            if not resolved.exists():
                errors.append(f"broken relative link: {document.path} -> {raw_link}")
        if document.document_type != "index" and document.indexed and document.path not in linked_from_index:
            debts.append(f"orphan testing document is not linked from {workspace.index}: {document.path}")

    definitions: dict[str, list[str]] = {}
    references: dict[str, list[str]] = {}
    module_t2: dict[str, dict[str, int]] = {}
    total_rows = 0
    for document in documents:
        text = (docs_dir / document.path).read_text(encoding="utf-8")
        rows = _case_rows(document, text)
        total_rows += len(rows)
        for row in rows:
            target = definitions if row["definition"] else references
            target.setdefault(row["case_id"], []).append(document.path)
            if row["definition"]:
                module = row["module"] or document.module or document.path
                stats = module_t2.setdefault(module, {"definitions": 0, "t2": 0, "main_path": 0, "boundary": 0})
                stats["definitions"] += 1
                if row["tier"].casefold() == "t2":
                    stats["t2"] += 1
                    role = re.sub(r"[\s_-]+", "", row["role"]).casefold()
                    if role in {"mainpath", "主路径", "核心路径", "happy", "happypath"}:
                        stats["main_path"] += 1
                    if role in {"boundary", "边界", "权限边界", "negative", "异常"}:
                        stats["boundary"] += 1

    for case_id, paths in sorted(definitions.items()):
        unique = sorted(set(paths))
        if len(unique) > 1:
            errors.append(f"duplicate canonical test case definition {case_id}: {unique}")
    for case_id, paths in sorted(references.items()):
        if case_id not in definitions:
            debts.append(f"test evidence/reference has no canonical definition {case_id}: {sorted(set(paths))}")

    for module, stats in sorted(module_t2.items()):
        if stats["definitions"] == 0:
            continue
        if stats["t2"] == 0:
            debts.append(f"module {module} has no T2-marked canonical test case")
        else:
            if stats["main_path"] == 0:
                debts.append(f"module {module} has no T2 main-path case")
            if stats["boundary"] == 0:
                debts.append(f"module {module} has no T2 boundary/permission case")

    valid = not errors and (not strict or not debts)
    return {
        "valid": valid,
        "strict": strict,
        "workspace": asdict(workspace),
        "summary": {
            "documents": len(documents),
            "canonical_cases": len(definitions),
            "referenced_cases": len(references),
            "case_rows": total_rows,
            "modules_with_cases": len(module_t2),
        },
        "documents": [asdict(document) for document in documents],
        "errors": list(dict.fromkeys(errors)),
        "warnings": list(dict.fromkeys(warnings)),
        "debts": list(dict.fromkeys(debts)),
    }


def _workspace_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--root", default=".")
    parser.add_argument("--config")
    parser.add_argument("--docs-root")
    parser.add_argument("--index")
    parser.add_argument("--entry")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage the Markdown-first testing documentation workspace")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("resolve", "ensure", "index", "validate"):
        command = sub.add_parser(name)
        _workspace_args(command)
        if name == "validate":
            command.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    kwargs = {
        "docs_root": args.docs_root,
        "index": args.index,
        "entry": args.entry,
        "config_path": Path(args.config) if args.config else None,
    }
    try:
        if args.command == "resolve":
            result = asdict(resolve_workspace(Path(args.root), **kwargs))
            code = 0
        elif args.command == "ensure":
            result = ensure_workspace(Path(args.root), **kwargs)
            code = 0
        elif args.command == "index":
            result = index_workspace(Path(args.root), **kwargs)
            code = 0
        else:
            result = validate_workspace(Path(args.root), strict=args.strict, **kwargs)
            code = 0 if result["valid"] else 1
    except (OSError, ConfigError, ValueError) as exc:
        result = {"valid": False, "errors": [str(exc)]}
        code = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
