#!/usr/bin/env python3
from __future__ import annotations

import base64
import lzma
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / '.github' / 'v024-patch-small'
SELF = ROOT / '.github' / 'apply_v024.py'
CI = ROOT / '.github' / 'workflows' / 'ci.yml'
WORKFLOW = ROOT / '.github' / 'workflows' / 'export-v024-workspace.yml'
OLD_PARTS = ROOT / '.github' / 'v024-parts'
OLD_BAD_PARTS = ROOT / '.github' / 'v024-patch-parts'


def run(*args: str, input_bytes: bytes | None = None) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, cwd=ROOT, input=input_bytes, check=True)


def main() -> None:
    chunks = sorted(path for path in PARTS.iterdir() if path.is_file())
    if not chunks:
        raise RuntimeError('v0.2.4 patch chunks are missing')
    encoded = ''.join(path.read_text(encoding='ascii').strip() for path in chunks)
    patch = lzma.decompress(base64.b64decode(encoded, validate=True))

    with tempfile.TemporaryDirectory() as temp:
        temp_root = Path(temp)
        original_ci = temp_root / 'ci.yml'
        original_workflow = temp_root / 'export-v024-workspace.yml'
        shutil.copy2(CI, original_ci)
        shutil.copy2(WORKFLOW, original_workflow)

        run('patch', '-p1', '--forward', '--batch', input_bytes=patch)
        for relative in ('adapters/claude-code/install.sh', 'adapters/codex/install.sh'):
            path = ROOT / relative
            path.chmod(path.stat().st_mode | 0o111)

        shutil.rmtree(PARTS)
        shutil.rmtree(OLD_PARTS, ignore_errors=True)
        shutil.rmtree(OLD_BAD_PARTS, ignore_errors=True)
        SELF.unlink(missing_ok=True)
        WORKFLOW.unlink(missing_ok=True)

        run('python', '-m', 'unittest', 'discover', '-s', 'tests', '-v')
        run('python', 'scripts/validate_bundle.py', '--root', '.')
        run('python', '-m', 'compileall', '-q', 'scripts', 'tests')
        run('bash', '-n', 'adapters/claude-code/install.sh')
        run('bash', '-n', 'adapters/codex/install.sh')
        run('python', 'scripts/siyk.py', 'config', 'validate', '--root', '.', '--file', 'assets/config.example.yaml', '--required')
        run('python', 'scripts/siyk.py', 'docs', 'resolve', '--root', '.')
        run('python', 'scripts/siyk.py', 'scan', '--root', '.', '--all')

        shutil.copy2(original_ci, CI)
        shutil.copy2(original_workflow, WORKFLOW)

    run('git', 'config', 'user.name', 'github-actions[bot]')
    run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    run('git', 'add', '-A')
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT).returncode == 0:
        raise RuntimeError('patch produced no repository changes')
    run('git', 'commit', '-m', 'feat: add Markdown-first testing documentation workspace')
    branch = os.environ.get('GITHUB_HEAD_REF') or os.environ.get('GITHUB_REF_NAME') or 'agent/v024-testing-docs'
    run('git', 'push', 'origin', f'HEAD:{branch}')


if __name__ == '__main__':
    main()
