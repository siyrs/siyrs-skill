#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
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
EXPECTED_PARTS = {
    'part-000': '1a270d16e482073ec3abec1df7a67a06f35625b53a04f1cc5e99b3fa1182689d',
    'part-001': 'fae45ba9b118e8a90ca7cdebaa2f913ba632e50fe3868ae7a40aa93d0d850680',
    'part-002': '9abe11d302f45f1b2138cd99f41d45504136d8ec7fe75eb7f6d0c25b8ab9617b',
    'part-003': '4bace3aac6ddb858d8c33ef9a79b4241b1fd54c6a8f34cdfa47eecd67a13c4fa',
    'part-004': '14d558d2b773a32c71012243e4cb3c7d28300f0f84366c8c15fbc3e3d5949228',
    'part-005': 'a0da6648f079f07f14cdef5b796a3ebe726e55414788605d80d92911bd22dc2a',
    'part-006': '8caaa2adc79ed472270b46ae8cb4838287d5f883c02b2fabf7ea30f275c36db8',
    'part-007': '9c9c97597c602f44daeef54370e0af1b0983b175c35993273e4c4b716feff0b5',
    'part-008': '4b1230b4dad215447904d0a99c54d808403d3b8b7aa3df878f3f5caf8919225f',
    'part-009': 'b96b1ff26c44767fb3910befa3d99600b99249a9fd54d865db72f23667cb6735',
    'part-010': '56b320dc05c0587258292ce8763718ee0389ae592f0b5bebb8bf4a6755022442',
    'part-011': '5210611fd8d7f20ce2893a316015ebc4683f4b50babb89da587790d645402d69',
    'part-012': 'bd005b44b0ab4a19c62306921d56813eeed81bdebe2e9c16b005ea51552e23d7',
    'part-013': 'cda2b1b2594fa6f208fa1eba8bf45b53ab203b3e8e95643b338f2535f423e230',
    'part-014': '4f66a527bf39613a7a3af887be87cee80cf7ffbc329361ec746836f88d9b2f0f',
    'part-015': '2e0970bbcfe08d3246f9ded18399ddf268931229f9a1ce370e1be65695c71fd9',
    'part-016': '5972c48a848af5c56f1c43e171b12bb868298bd93c222825c87fac763ddd90ed',
    'part-017': 'db5e651ebc7b1a06aa74134ca6f0ccd49d0525cc6144fe87e30249e93f83c5dd',
    'part-018': '3c79f5e7a767075ab35a2f1b564ee78dc4ec63905deaa2759e55315228f6c85e',
    'part-019': 'bc46a702c41c58ab7cad6642c67f7f08befe0853f7648045c5908c65f325f0bc',
    'part-020': '8d25459e878c4e9e0f6c5bb0b228e956bb8ea7eaaf0a4faf83b327efb657a26a',
    'part-021': 'b6f658f57ba8009971297895becc4bf327bf914156f3ae414785f3487c38891d',
    'part-022': 'b86ba4be6b28b4200467e4efc4cc0520b47d053efdf385f16b1884d9a7dcdcb6',
    'part-023': '0bcaba5e0e1508ae99d1b6c82b4385ef0d0085365293dcb71f75b9e11433080a',
    'part-024': '7c5e8e315fa912fade788d4cffdcba708796fba4832d9697b5e27889eb351dcb',
    'part-025': 'c31d1772a12757909f895d6a1bc1b0500a33560132780a9f98a040fc03d48a4e',
    'part-026': '76383c04f8ad8f892dbfe497b40baefd3962aedb65af437b77afa0c379c683f6',
    'part-027': 'cb58d6f550ee9d95a849f80b664367f9c84ed53895f5a10b77acb0a147797ba5',
    'part-028': '36f753152590ecef0196c03e584bfac181f9ab9b4795c554898606561c9e39af',
    'part-029': '5035315decd9473b425f727e6c5dec044767a2b4a99aaa56e0898b2b7f4fe247',
    'part-030': '7ba8d7a58e870a50772b12d827f2ce4d7c3e5362b1f1874eb348d7430bd4b0af',
    'part-031': '3e666e930272cefa07db26db02683f9967dab05d8ae9067099c78bfd4e526bc4',
    'part-032': '859efe1a5714b2b68afe524fa5df2b212cc63ea462750209e34a599b30203a8d',
    'part-033': '7071264bcacbaade7f37cf32d7c94fc36a2a92d9b79ee89de47c0f16d0d54658',
    'part-034': '8ee6b52d605bcbf46e773316796485fe6551c1731b327ac0a7088bae32675991',
    'part-035': '286f8dd61b616052bfbbae7856d38f57a7bfd8d958b7c7d52ecd19e53a979dd5',
}
EXPECTED_ENCODED_SHA256 = '2e5958ce4c500e21aba15483eea375ec62ebae14e95ad63094ddbac8a26e9023'
EXPECTED_ENCODED_LENGTH = 35340


def run(*args: str, input_bytes: bytes | None = None) -> None:
    print('+', ' '.join(args), flush=True)
    subprocess.run(args, cwd=ROOT, input=input_bytes, check=True)


def main() -> None:
    chunks = sorted(path for path in PARTS.iterdir() if path.is_file())
    if not chunks:
        raise RuntimeError('v0.2.4 patch chunks are missing')
    mismatches = []
    for path in chunks:
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        expected = EXPECTED_PARTS.get(path.name)
        if actual != expected:
            mismatches.append(f'{path.name}: expected={expected} actual={actual}')
    if mismatches or set(path.name for path in chunks) != set(EXPECTED_PARTS):
        raise RuntimeError('patch part verification failed: ' + '; '.join(mismatches) + f'; files={[path.name for path in chunks]}')
    encoded = ''.join(path.read_text(encoding='ascii').strip() for path in chunks)
    encoded_sha = hashlib.sha256(encoded.encode('ascii')).hexdigest()
    if len(encoded) != EXPECTED_ENCODED_LENGTH or encoded_sha != EXPECTED_ENCODED_SHA256:
        raise RuntimeError(f'encoded payload mismatch: length={len(encoded)} sha256={encoded_sha}')
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
