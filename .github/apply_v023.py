#!/usr/bin/env python3
from __future__ import annotations

import base64
import io
import os
import shutil
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARTS = ROOT / '.github' / 'v023-parts'
SELF = ROOT / '.github' / 'apply_v023.py'
WORKFLOW = ROOT / '.github' / 'workflows' / 'apply-v023.yml'


def run(*args: str) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, cwd=ROOT, check=True)


def safe_extract(payload: bytes) -> None:
    root = ROOT.resolve()
    with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk():
                raise RuntimeError(f'archive links are not allowed: {member.name}')
            target = (ROOT / member.name).resolve()
            try:
                target.relative_to(root)
            except ValueError as exc:
                raise RuntimeError(f'archive path escapes repository: {member.name}') from exc
        archive.extractall(ROOT)


def main() -> None:
    chunks = sorted(path for path in PARTS.iterdir() if path.is_file())
    if not chunks:
        raise RuntimeError('v0.2.3 payload chunks are missing')
    encoded = ''.join(path.read_text(encoding='ascii').strip() for path in chunks)
    safe_extract(base64.b64decode(encoded, validate=True))

    for relative in ('adapters/claude-code/install.sh', 'adapters/codex/install.sh'):
        path = ROOT / relative
        path.chmod(path.stat().st_mode | 0o111)

    shutil.rmtree(PARTS)
    SELF.unlink(missing_ok=True)
    WORKFLOW.unlink(missing_ok=True)

    run('python', '-m', 'unittest', 'discover', '-s', 'tests', '-v')
    run('python', 'scripts/validate_bundle.py', '--root', '.')
    run('python', '-m', 'compileall', '-q', 'scripts', 'tests')
    run('bash', '-n', 'adapters/claude-code/install.sh')
    run('bash', '-n', 'adapters/codex/install.sh')
    run('python', 'scripts/siyk.py', 'config', 'validate', '--root', '.', '--file', 'assets/config.example.yaml', '--required')
    run('python', 'scripts/siyk.py', 'scan', '--root', '.', '--all')

    run('git', 'config', 'user.name', 'github-actions[bot]')
    run('git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
    run('git', 'add', '-A')
    status = subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=ROOT)
    if status.returncode == 0:
        raise RuntimeError('payload produced no repository changes')
    run('git', 'commit', '-m', 'feat: close v0.2.3 runtime governance gaps')
    branch = os.environ.get('GITHUB_HEAD_REF') or os.environ.get('GITHUB_REF_NAME') or 'agent/v023-runtime-closure'
    run('git', 'push', 'origin', f'HEAD:{branch}')


if __name__ == '__main__':
    main()
