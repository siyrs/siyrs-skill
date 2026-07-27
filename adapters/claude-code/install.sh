#!/usr/bin/env bash
set -euo pipefail

adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
skill_source="$(cd "${adapter_dir}/../.." && pwd)"
claude_home="${CLAUDE_HOME:-${HOME}/.claude}"
skill_target="${claude_home}/skills/siyrs-skill"
command_target="${claude_home}/commands"

mkdir -p "$(dirname "${skill_target}")" "${command_target}"
source_real="$(python -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "${skill_source}")"
target_real="$(python -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "${skill_target}")"

if [[ "${source_real}" != "${target_real}" ]]; then
  temp_target="${skill_target}.tmp.$$"
  trap 'rm -rf "${temp_target:-}"' EXIT
  rm -rf "${temp_target}"
  cp -R "${skill_source}" "${temp_target}"
  rm -rf "${temp_target}/.git" "${temp_target}/__pycache__" "${temp_target}/.pytest_cache"
  find "${temp_target}" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "${temp_target}" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
  rm -rf "${skill_target}"
  mv "${temp_target}" "${skill_target}"
  trap - EXIT
fi
cp "${adapter_dir}"/commands/*.md "${command_target}/"

echo "Installed siyrs-skill to ${skill_target}"
echo "Installed /siyk-* command adapters to ${command_target}"
