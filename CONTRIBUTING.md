# Contributing

Keep this repository deliberately small.

- Keep `SKILL.md` concise, imperative, and under 500 lines; target substantially less.
- Put optional detail in one-level `references/` files and link them directly from `SKILL.md`.
- Add scripts only for repeated deterministic work; prefer repository-native tools for engineering tasks.
- Do not reintroduce per-agent adapters, slash-command registries, state machines, configuration schemas, release manifests, or generated documentation trees for ordinary workflows.
- Update `agents/openai.yaml` when the skill name, description, or intended default invocation changes.
- Run `python scripts/validate.py .` and `python -m unittest discover -s tests -v` before merging.
