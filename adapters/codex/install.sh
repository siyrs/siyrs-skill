#!/usr/bin/env bash
set -euo pipefail
adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
skill_source="$(cd "${adapter_dir}/../.." && pwd -P)"
skills_home="${SIYRS_CODEX_SKILLS_HOME:-${HOME}/.agents/skills}"
archive_home="${SIYRS_CODEX_SKILL_BACKUPS_HOME:-$(dirname "${skills_home}")/skill-backups}"
python_cmd="${PYTHON:-}"
if [[ -z "${python_cmd}" ]]; then
  if command -v python3 >/dev/null 2>&1; then python_cmd=python3; else python_cmd=python; fi
fi
entrypoints=()
legacy_names=()
while IFS= read -r value; do [[ -n "${value}" ]] && entrypoints+=("${value}"); done < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field names)
while IFS= read -r value; do [[ -n "${value}" ]] && legacy_names+=("${value}"); done < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field legacy-names)
mkdir -p "${skills_home}" "${archive_home}"
skills_home="$(cd "${skills_home}" && pwd -P)"
archive_home="$(cd "${archive_home}" && pwd -P)"
core_target="${skills_home}/siyrs-skill"
case "${skills_home}/" in "${skill_source}/"*) echo "Refusing install inside source" >&2; exit 2;; esac
case "${archive_home}/" in "${skills_home}/"*) echo "Archive must be outside discovery directory" >&2; exit 5;; esac
archive_dir() {
  source_path="$1"; label="$2"
  [[ -e "${source_path}" ]] || return 0
  stamp="$(date +%Y%m%d-%H%M%S)"; target="${archive_home}/${label}-${stamp}"; suffix=1
  while [[ -e "${target}" ]]; do target="${archive_home}/${label}-${stamp}-${suffix}"; suffix=$((suffix + 1)); done
  mv "${source_path}" "${target}"
  echo "Archived ${source_path} -> ${target}"
}
# Python provides a portable direct-child directory listing on macOS/Linux/Git Bash.
while IFS= read -r candidate; do
  [[ -d "${candidate}" ]] || continue
  name="$(basename "${candidate}")"
  [[ "${name}" == "siyrs-skill" ]] && continue
  manifest="${candidate}/SKILL.md"
  if [[ -f "${manifest}" ]] && grep -Eq '^name:[[:space:]]*siyrs-skill[[:space:]]*$' "${manifest}"; then
    archive_dir "${candidate}" "siyrs-skill-duplicate"
  fi
done < <("${python_cmd}" - "${skills_home}" <<'PY'
from pathlib import Path
import sys
for child in sorted(Path(sys.argv[1]).iterdir()):
    if child.is_dir():
        print(child)
PY
)
for name in "${legacy_names[@]}"; do archive_dir "${skills_home}/${name}" "siyrs-entrypoint-${name}"; done
stage_root="$(mktemp -d "${skills_home}/.siyrs-codex-install.XXXXXX")"
trap 'rm -rf "${stage_root}"' EXIT
install_core=true
if [[ -d "${core_target}" ]] && [[ "$(cd "${core_target}" && pwd -P)" == "${skill_source}" ]]; then install_core=false; fi
if [[ "${install_core}" == true ]]; then
  mkdir -p "${stage_root}/siyrs-skill"
  cp -R "${skill_source}/." "${stage_root}/siyrs-skill/"
  rm -rf "${stage_root}/siyrs-skill/.git" "${stage_root}/siyrs-skill/__pycache__" "${stage_root}/siyrs-skill/.pytest_cache"
  find "${stage_root}/siyrs-skill" -type d -name __pycache__ -prune -exec rm -rf {} \;
  find "${stage_root}/siyrs-skill" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
fi
for name in "${entrypoints[@]}"; do
  src="${adapter_dir}/entrypoints/${name}"; template="${src}/SKILL.template.md"; target="${stage_root}/${name}"
  [[ -f "${template}" ]] || { echo "Missing ${name} template" >&2; exit 3; }
  mkdir -p "${target}"; cp "${template}" "${target}/SKILL.md"
  [[ -d "${src}/agents" ]] && cp -R "${src}/agents" "${target}/agents"
  grep -Eq "^name:[[:space:]]*${name}[[:space:]]*$" "${target}/SKILL.md" || exit 4
done
replace_target() { rm -rf "${skills_home}/$1"; mv "${stage_root}/$1" "${skills_home}/$1"; }
[[ "${install_core}" == true ]] && replace_target siyrs-skill
for name in "${entrypoints[@]}"; do replace_target "${name}"; done
echo "Installed siyrs-skill core and entrypoints: ${entrypoints[*]}"
