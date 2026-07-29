#!/usr/bin/env bash
set -euo pipefail
adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
skill_source="$(cd "${adapter_dir}/../.." && pwd -P)"
skills_home="${SIYRS_CODEX_SKILLS_HOME:-${HOME}/.agents/skills}"
archive_home="${SIYRS_CODEX_SKILL_BACKUPS_HOME:-$(dirname "${skills_home}")/skill-backups}"
python_cmd="${PYTHON:-}"
if [[ -z "${python_cmd}" ]]; then command -v python3 >/dev/null && python_cmd=python3 || python_cmd=python; fi
mapfile -t entrypoints < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field names)
mapfile -t legacy_names < <("${python_cmd}" "${skill_source}/scripts/command_registry.py" --root "${skill_source}" --field legacy-names)
mkdir -p "${skills_home}" "${archive_home}"
skills_home="$(cd "${skills_home}" && pwd -P)"; archive_home="$(cd "${archive_home}" && pwd -P)"
core_target="${skills_home}/siyrs-skill"
case "${skills_home}/" in "${skill_source}/"*) echo "Refusing install inside source" >&2; exit 2;; esac
case "${archive_home}/" in "${skills_home}/"*) echo "Archive must be outside discovery directory" >&2; exit 5;; esac
archive_dir(){
  local source="$1" label="$2" stamp target suffix=1
  [[ -e "$source" ]] || return 0
  stamp="$(date +%Y%m%d-%H%M%S)"; target="${archive_home}/${label}-${stamp}"
  while [[ -e "$target" ]]; do target="${archive_home}/${label}-${stamp}-${suffix}"; suffix=$((suffix+1)); done
  mv "$source" "$target"; echo "Archived $source -> $target"
}
# Archive duplicate roots not using the canonical directory.
while IFS= read -r -d '' candidate; do
  name="$(basename "$candidate")"; [[ "$name" == "siyrs-skill" ]] && continue
  manifest="$candidate/SKILL.md"
  if [[ -f "$manifest" ]] && grep -Eq '^name:[[:space:]]*siyrs-skill[[:space:]]*$' "$manifest"; then archive_dir "$candidate" "siyrs-skill-duplicate"; fi
done < <(find "$skills_home" -mindepth 1 -maxdepth 1 -type d -print0)
# Archive deprecated entrypoints so old picker entries disappear after upgrade.
for name in "${legacy_names[@]}"; do archive_dir "${skills_home}/${name}" "siyrs-entrypoint-${name}"; done
stage_root="$(mktemp -d "${skills_home}/.siyrs-codex-install.XXXXXX")"; trap 'rm -rf "${stage_root}"' EXIT
install_core=true
if [[ -d "$core_target" ]] && [[ "$(cd "$core_target" && pwd -P)" == "$skill_source" ]]; then install_core=false; fi
if [[ "$install_core" == true ]]; then
  mkdir -p "$stage_root/siyrs-skill"; cp -R "$skill_source/." "$stage_root/siyrs-skill/"
  rm -rf "$stage_root/siyrs-skill/.git" "$stage_root/siyrs-skill/__pycache__" "$stage_root/siyrs-skill/.pytest_cache"
  find "$stage_root/siyrs-skill" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "$stage_root/siyrs-skill" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
fi
for name in "${entrypoints[@]}"; do
  src="$adapter_dir/entrypoints/$name"; [[ -f "$src/SKILL.template.md" ]] || { echo "Missing $name template" >&2; exit 3; }
  mkdir -p "$stage_root/$name"; cp "$src/SKILL.template.md" "$stage_root/$name/SKILL.md"
  [[ -d "$src/agents" ]] && cp -R "$src/agents" "$stage_root/$name/agents"
  grep -Eq "^name:[[:space:]]*${name}[[:space:]]*$" "$stage_root/$name/SKILL.md" || exit 4
done
replace(){ rm -rf "$skills_home/$1"; mv "$stage_root/$1" "$skills_home/$1"; }
[[ "$install_core" == true ]] && replace siyrs-skill
for name in "${entrypoints[@]}"; do replace "$name"; done
echo "Installed siyrs-skill core and entrypoints: ${entrypoints[*]}"
