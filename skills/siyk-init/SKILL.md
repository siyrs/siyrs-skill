---
name: siyk-init
description: 显式的项目初始化与刷新快捷 Skill。用于创建或刷新 `<project-root>/.siyrs/README.md` 项目地图，记录模块、技术栈、测试入口、文档、常用命令和索引基准 commit，减少后续重复全仓扫描；不创建状态机、registry、cache，也不保存 secret 值。
---

# SIYK 项目初始化

开始前读取并遵循 [SIYRS 第一性原则](../../references/principles.md)。

只维护 `.siyrs/README.md` 项目地图，然后结束。

1. 优先用 Git top-level 识别 project root；没有 Git 时使用当前明确项目根目录。
2. 如果 `.siyrs/README.md` 已存在，先读取并把本次操作视为刷新，不创建第二套索引。
3. 做结构级扫描：根 README / AGENTS、主要模块、构建文件、测试目录与框架、`docs/testing/`、CI、Docker/compose、运行入口和可确认的常用命令。
4. 默认跳过 `.git/`、`node_modules/`、`target/`、`dist/`、`build/`、`coverage/`、依赖缓存和二进制生成物；不要为了建索引遍历全部源码。
5. 创建或更新 `.siyrs/README.md`，至少在有真实信息时记录项目、模块、关键路径、测试代码位置、重要文档、常用命令、运行/CI 入口和当前 Git HEAD commit SHA。
6. 文件开头明确说明：项目地图只用于快速定位，真实代码、构建配置、测试代码和项目文档始终优先。
7. 可以记录 `.env` 等配置入口的存在，但禁止把密码、token、API key、cookie、私钥或其他 secret 值写入 `.siyrs`。
8. 只使用 Markdown。不要创建 `manifest.json`、`state.json`、`registry.json`、`cache/` 或新的运行时框架。
9. 不复制源码、测试用例正文、P0/P1/P2/P3 全文、release gate、测试报告或 Git 历史；只保存导航所需的摘要和相对链接。
10. 不修改项目测试代码布局，不迁移 E2E，不 commit、不 push、不 release、不 deploy，除非同一请求另外明确要求这些工作。

重复调用 `/siyk-init` 的语义就是重新检查稳定项目结构并刷新同一个 `.siyrs/README.md`。索引基准 commit 只是新鲜度提示，不是 gate。
