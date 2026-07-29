#!/usr/bin/env python3
"""Validate structure, command registry, adapters, schemas, CI, and release contract."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from command_registry import load_registry, parse_frontmatter

IGNORED_PARTS={'.git','__pycache__','.pytest_cache','.mypy_cache','.ruff_cache'}
IGNORED_SUFFIXES={'.pyc','.pyo'}
REQUIRED_STATIC={
 'VERSION','SKILL.md','README.md','CHANGELOG.md','release-manifest.json',
 'references/testing-common.md','references/testing-tiers.md','references/testing-selectors.md',
 'references/git-policy.md','references/git-content-scan.md','references/risk-authorization.md',
 'references/subworkflow-composition.md','references/safety-and-authorization.md','references/output-contract.md',
 'scripts/command_registry.py','scripts/route_command.py','scripts/collect_git_changes.py','scripts/state.py',
 'scripts/validate_bundle.py','schemas/config.schema.json','schemas/state.schema.json',
 'assets/config.example.yaml','assets/state.example.json','assets/templates/TEST-MATRIX.template.md',
 '.github/workflows/ci.yml','adapters/claude-code/install.sh','adapters/claude-code/install.ps1',
 'adapters/codex/install.sh','adapters/codex/install.ps1','docs/RELEASE-REPORT-v0.2.2.md'
}

def actual_files(root:Path)->list[str]:
    out=[]
    for p in root.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(root)
        if any(x in IGNORED_PARTS for x in rel.parts): continue
        if p.suffix in IGNORED_SUFFIXES or p.name=='.DS_Store': continue
        out.append(rel.as_posix())
    return sorted(out)

def read_json(path:Path,errors:list[str]):
    try: data=json.loads(path.read_text(encoding='utf-8'))
    except (OSError,json.JSONDecodeError) as exc: errors.append(f'invalid JSON {path}: {exc}'); return None
    if not isinstance(data,dict): errors.append(f'JSON root must be object: {path}'); return None
    return data

def version_from(text:str,pattern:str)->str|None:
    m=re.search(pattern,text,re.M); return m.group(1) if m else None

def validate(root:Path)->dict:
    root=root.resolve(); errors=[]; warnings=[]
    for rel in sorted(REQUIRED_STATIC):
        if not (root/rel).is_file(): errors.append(f'missing required file: {rel}')
    skills=[p for p in root.rglob('*') if p.is_file() and p.name.lower()=='skill.md' and not any(x in IGNORED_PARTS for x in p.relative_to(root).parts)]
    if len(skills)!=1: errors.append(f'expected exactly one source SKILL.md, found {len(skills)}')
    version=(root/'VERSION').read_text(encoding='utf-8').strip() if (root/'VERSION').is_file() else None
    if version and not re.fullmatch(r'\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?',version): errors.append(f'invalid VERSION: {version!r}')
    try: specs=load_registry(root)
    except (OSError,ValueError) as exc: errors.append(f'invalid command registry: {exc}'); specs=[]
    commands=[s.command for s in specs]; names=[s.name for s in specs if s.client_entrypoint]; legacy=sorted({x for s in specs for x in s.legacy_commands}); legacy_names=[x.removeprefix('/') for x in legacy]
    if len(specs)!=6: errors.append(f'expected six commands, found {len(specs)}')
    skill=(root/'SKILL.md').read_text(encoding='utf-8') if (root/'SKILL.md').is_file() else ''
    try:
        fm,_=parse_frontmatter(root/'SKILL.md', {'name', 'description'})
        if fm.get('name')!='siyrs-skill': errors.append('root frontmatter name must be siyrs-skill')
    except (OSError,ValueError) as exc: errors.append(str(exc))
    for cmd in commands:
        if cmd not in skill: errors.append(f'root SKILL.md omits {cmd}')
    if version and version_from(skill,r'^Version:\s*\*\*(\S+)\*\*\s*$')!=version: errors.append('SKILL.md version drift')
    readme=(root/'README.md').read_text(encoding='utf-8') if (root/'README.md').is_file() else ''
    changelog=(root/'CHANGELOG.md').read_text(encoding='utf-8') if (root/'CHANGELOG.md').is_file() else ''
    if version and version_from(readme,r'当前版本：`v([^`]+)`')!=version: errors.append('README version drift')
    if version and version_from(changelog,r'^##\s+([0-9][^\s]*)\s+-\s+')!=version: errors.append('CHANGELOG version drift')
    manifest=read_json(root/'release-manifest.json',errors) if (root/'release-manifest.json').is_file() else None
    if manifest:
        if manifest.get('version')!=version: errors.append('release-manifest version drift')
        if manifest.get('commands')!=commands: errors.append('release-manifest commands differ from Markdown registry')
        declared=manifest.get('files')
        if not isinstance(declared,list) or not all(isinstance(x,str) for x in declared): errors.append('release-manifest files must be string array')
        else:
            if len(declared)!=len(set(declared)): errors.append('release-manifest files duplicate')
            actual=actual_files(root); omitted=sorted(set(actual)-set(declared)); missing=sorted(set(declared)-set(actual))
            if omitted: errors.append(f'release-manifest omits files: {omitted}')
            if missing: errors.append(f'release-manifest references missing files: {missing}')
    # Adapters must be exact; stale source adapters are a release error.
    claude_dir=root/'adapters/claude-code/commands'
    claude={p.stem for p in claude_dir.glob('*.md')} if claude_dir.is_dir() else set()
    if claude!=set(names): errors.append(f'Claude adapter set mismatch: actual={sorted(claude)} expected={sorted(names)}')
    for name in names:
        p=claude_dir/f'{name}.md'; text=p.read_text(encoding='utf-8') if p.is_file() else ''
        if f'/{name}' not in text or '$ARGUMENTS' not in text or 'siyrs-skill-command-adapter: true' not in text: errors.append(f'invalid Claude adapter: {name}')
        tpl=root/'adapters/codex/entrypoints'/name/'SKILL.template.md'; meta=root/'adapters/codex/entrypoints'/name/'agents/openai.yaml'
        if not tpl.is_file() or not meta.is_file(): errors.append(f'missing Codex entrypoint: {name}'); continue
        tt=tpl.read_text(encoding='utf-8'); mt=meta.read_text(encoding='utf-8')
        if not re.search(rf'(?m)^name:\s*{re.escape(name)}\s*$',tt): errors.append(f'Codex name mismatch: {name}')
        if '<skills-root>/siyrs-skill/SKILL.md' not in tt or f'/{name}' not in tt: errors.append(f'Codex delegation mismatch: {name}')
        if f'display_name: "/{name}"' not in mt or 'allow_implicit_invocation: false' not in mt: errors.append(f'Codex metadata mismatch: {name}')
    codex_dirs={p.name for p in (root/'adapters/codex/entrypoints').iterdir() if p.is_dir()} if (root/'adapters/codex/entrypoints').is_dir() else set()
    if codex_dirs!=set(names): errors.append(f'Codex entrypoint set mismatch: actual={sorted(codex_dirs)} expected={sorted(names)}')
    # CI and installers must use current registry and not deprecated names.
    ci=(root/'.github/workflows/ci.yml').read_text(encoding='utf-8') if (root/'.github/workflows/ci.yml').is_file() else ''
    for name in names:
        if name not in ci: errors.append(f'CI omits current command {name}')
    for old in legacy:
        if re.search(rf'siyk\.py\s+route\s+[\"\']?{re.escape(old)}(?:\s|[\"\'])', ci):
            errors.append(f'CI executes deprecated command {old}')
    for rel in ('adapters/claude-code/install.sh','adapters/claude-code/install.ps1','adapters/codex/install.sh','adapters/codex/install.ps1'):
        text=(root/rel).read_text(encoding='utf-8') if (root/rel).is_file() else ''
        if 'command_registry.py' not in text: errors.append(f'installer does not consume Markdown registry: {rel}')
    # Schemas/examples v2.
    config=read_json(root/'schemas/config.schema.json',errors); state_schema=read_json(root/'schemas/state.schema.json',errors); state_example=read_json(root/'assets/state.example.json',errors)
    if config and config.get('properties',{}).get('version',{}).get('const')!=2: errors.append('config schema must be v2')
    if state_schema and state_schema.get('properties',{}).get('version',{}).get('const')!=2: errors.append('state schema must be v2')
    if state_example and state_example.get('version')!=2: errors.append('state example must be v2')
    config_text=(root/'assets/config.example.yaml').read_text(encoding='utf-8') if (root/'assets/config.example.yaml').is_file() else ''
    for token in ('version: 2','tiers:','t1:','t2:','t3:','preflight:'): 
        if token not in config_text: errors.append(f'config example missing {token}')
    matrix=(root/'assets/templates/TEST-MATRIX.template.md').read_text(encoding='utf-8') if (root/'assets/templates/TEST-MATRIX.template.md').is_file() else ''
    for token in ('Tier','Selector/Test ID','Role'):
        if token not in matrix: errors.append(f'TEST-MATRIX template missing {token}')
    architecture=(root/'docs/ARCHITECTURE.md').read_text(encoding='utf-8') if (root/'docs/ARCHITECTURE.md').is_file() else ''
    if 'six stable commands' not in architecture.lower(): errors.append('architecture does not describe six stable commands')
    return {'root':str(root),'version':version,'valid':not errors,'commands':commands,'legacy_commands':legacy,'files':len(actual_files(root)),'errors':errors,'warnings':warnings}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--root',default='.'); a=p.parse_args(); r=validate(Path(a.root)); print(json.dumps(r,ensure_ascii=False,indent=2)); return 0 if r['valid'] else 1
if __name__=='__main__': raise SystemExit(main())
