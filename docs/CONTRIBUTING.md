# 贡献指南

## 1. 先理解文档层级

- `skills/*/SKILL.md`：独立 Skill 行为入口。
- `skills/*/references/`：已物化的运行时 Markdown，只由同步工具维护。
- `shared/references/`：跨 Skill 共享规范的唯一人工维护源。
- `skills/*/agents/openai.yaml`：Codex 展示与调用策略。
- `README.md` / `docs/*.md`：安装、架构、维护和计划说明，不承载运行时唯一规则。

## 2. 修改共享规则

修改 `shared/references/*.md` 后执行：

```bash
python scripts/sync_references.py
python scripts/sync_references.py --check
```

不要直接编辑 `skills/*/references/`；CI 会检查内容漂移、多余文件和缺失引用。

## 3. 修改或新增 Skill

每个 Skill 必须：

- 位于 `skills/<name>/`；
- 包含 `SKILL.md`；
- `name` 与父目录完全一致；
- frontmatter 源码只使用 Agent Skills 标准字段；
- 所有运行时链接都留在 Skill 根目录内；
- 包含 `agents/openai.yaml`；
- 主 `siyrs-skill` 使用 `allow_implicit_invocation: true`；
- `siyk-*` 使用 `allow_implicit_invocation: false`。

显式 `siyk-*` 的 description 应简短，说明用途即可；复杂判断留在正文。主 Skill description 需要覆盖通用工程任务关键词，便于自动选择。

引用共享规范时写：

```markdown
[测试指南](references/testing.md)
```

然后在 `shared/references/testing.md` 维护权威内容并运行同步工具。

## 4. Claude Code 扩展

不要把 `disable-model-invocation` 直接写进源码 `SKILL.md`。Claude Code 变体由 `scripts/install.py` 在 `.generated/claude/skills/` 中确定性生成。

不要恢复 `.claude-plugin/`：Plugin namespace 不满足本项目需要的直接 `/siyrs-skill` 与 `/siyk-*` 入口。

## 5. 何时可以增加脚本

只有以下工作适合脚本化：

- 共享 Markdown 的确定性同步；
- 跨平台安装映射；
- 结构和一致性校验；
- 其他明确重复、确定且机器执行更可靠的工作。

不要用脚本重新编码自然语言业务规则，也不要增加 router、state、schema、registry、matrix runtime 或 adapter 业务副本。

## 6. 本地验证

```bash
python scripts/sync_references.py --check
python scripts/validate.py .
python -m unittest discover -s tests -v
python -m compileall -q scripts tests
```

还应生成 Claude Code 变体验证：

```bash
python scripts/install.py --build-claude .generated/claude/skills
```

Windows 可使用 `py` 替代 `python`。

## 7. 版本与文档

发布版本时同步更新：

- `VERSION`；
- 根 `README.md` 的当前版本；
- `docs/CHANGELOG.md`；
- 必要的架构/安装说明。

不要为了版本变化修改目标项目的 `.siyrs/`、`docs/testing/` 或历史测试 Case。
