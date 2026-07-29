#!/usr/bin/env bash
set -euo pipefail
adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
skill_source="$(cd "${adapter_dir}/../.." && pwd -P)"
claude_home="${CLAUDE_HOME:-${HOME}/.claude}"
skill_target="${claude_home}/skills/siyrs-skill"
command_target="${claude_home}/commands"
python_cmd="${PYTHON:-}"
if [[ -z "${python_cmd}" ]]; then command -v python3 >/dev/null && python_cmd=python3 || python_cmd=python; fi
mapfile -t names < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field names)
mapfile -t legacy_names < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field legacy-names)
mkdir -p "$(dirname "${skill_target}")" "${command_target}"
source_real="$("${python_cmd}" -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "${skill_source}")"
target_real="$("${python_cmd}" -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "${skill_target}")"
if [[ "${source_real}" != "${target_real}" ]]; then
  temp_target="${skill_target}.tmp.$$"; trap 'rm -rf "${temp_target:-}"' EXIT
  rm -rf "${temp_target}"; cp -R "${skill_source}" "${temp_target}"
  rm -rf "${temp_target}/.git" "${temp_target}/__pycache__" "${temp_target}/.pytest_cache"
  find "${temp_target}" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "${temp_target}" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
  rm -rf "${skill_target}"; mv "${temp_target}" "${skill_target}"; trap - EXIT
fi
for name in "${names[@]}" "${legacy_names[@]}"; do rm -f "${command_target}/${name}.md"; done
while IFS= read -r -d '' file; do
  grep -q '^siyrs-skill-command-adapter:[[:space:]]*true' "${file}" && rm -f "${file}"
done < <(find "${command_target}" -maxdepth 1 -type f -name 'siyk-*.md' -print0)
for name in "${names[@]}"; do cp "${adapter_dir}/commands/${name}.md" "${command_target}/${name}.md"; done
echo "Installed siyrs-skill and commands: ${names[*]}"
