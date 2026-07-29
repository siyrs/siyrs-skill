#!/usr/bin/env bash
set -euo pipefail

adapter_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
skill_source="$(cd "${adapter_dir}/../.." && pwd -P)"
skills_home="${SIYRS_CODEX_SKILLS_HOME:-${HOME}/.agents/skills}"
entrypoints=(siyk-test-full siyk-test-new siyk-git-commit siyk-git-sync)

mkdir -p "${skills_home}"
skills_home="$(cd "${skills_home}" && pwd -P)"
core_target="${skills_home}/siyrs-skill"

case "${skills_home}/" in
  "${skill_source}/"*)
    echo "Refusing to install inside the source repository: ${skills_home}" >&2
    exit 2
    ;;
esac

stage_root="$(mktemp -d "${skills_home}/.siyrs-codex-install.XXXXXX")"
cleanup() { rm -rf "${stage_root}"; }
trap cleanup EXIT

install_core=true
if [[ -d "${core_target}" ]]; then
  core_real="$(cd "${core_target}" && pwd -P)"
  if [[ "${core_real}" == "${skill_source}" ]]; then
    install_core=false
  fi
fi

if [[ "${install_core}" == true ]]; then
  mkdir -p "${stage_root}/siyrs-skill"
  cp -R "${skill_source}/." "${stage_root}/siyrs-skill/"
  rm -rf "${stage_root}/siyrs-skill/.git" \
         "${stage_root}/siyrs-skill/__pycache__" \
         "${stage_root}/siyrs-skill/.pytest_cache"
  find "${stage_root}/siyrs-skill" -type d -name __pycache__ -prune -exec rm -rf {} +
  find "${stage_root}/siyrs-skill" -type f \( -name '*.pyc' -o -name '*.pyo' \) -delete
fi

for name in "${entrypoints[@]}"; do
  source_dir="${adapter_dir}/entrypoints/${name}"
  template="${source_dir}/SKILL.template.md"
  target_stage="${stage_root}/${name}"
  [[ -f "${template}" ]] || { echo "Missing entrypoint template: ${template}" >&2; exit 3; }
  mkdir -p "${target_stage}"
  cp "${template}" "${target_stage}/SKILL.md"
  if [[ -d "${source_dir}/agents" ]]; then
    cp -R "${source_dir}/agents" "${target_stage}/agents"
  fi
  grep -Eq "^name:[[:space:]]*${name}[[:space:]]*$" "${target_stage}/SKILL.md" || {
    echo "Invalid entrypoint name in ${template}" >&2
    exit 4
  }
done

replace_target() {
  local name="$1"
  local staged="${stage_root}/${name}"
  local target="${skills_home}/${name}"
  rm -rf "${target}"
  mv "${staged}" "${target}"
}

if [[ "${install_core}" == true ]]; then
  replace_target siyrs-skill
fi
for name in "${entrypoints[@]}"; do
  replace_target "${name}"
done

legacy="${HOME}/.codex/skills/siyrs-skill"
if [[ -e "${legacy}" ]]; then
  echo "Note: legacy Codex Skill found at ${legacy}; remove it manually after verifying the new install." >&2
fi

echo "Installed siyrs-skill core to ${core_target}"
echo "Installed Codex entrypoints: ${entrypoints[*]}"
echo "Restart Codex if /siyk autocomplete does not refresh immediately."
