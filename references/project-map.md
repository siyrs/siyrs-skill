# `.siyrs` 项目地图指南

`.siyrs/README.md` 用于让 AI / Agent 快速理解项目结构并定位真实资料，减少每轮都从仓库根目录重新全局扫描的成本。

它是**项目地图和导航索引**，不是新的配置中心、状态数据库或事实缓存。

## 权威性

`.siyrs/README.md` 开头必须明确说明：

> 本文件用于快速理解项目结构和定位资料。真实代码、构建配置、测试代码和项目文档始终优先于本索引。

Agent 可以先读它定位目标，但涉及本轮修改时仍要打开相关真实文件确认现状。

## `/siyk-init` 做什么

首次调用时创建 `.siyrs/README.md`；再次调用时重新检查稳定项目结构并刷新同一文件。

优先识别：

- project root 与项目名称；
- 主要模块及相对路径；
- 各模块技术栈和关键构建文件，例如 `package.json`、`pom.xml`、`build.gradle`、`pyproject.toml`；
- 可执行测试代码位置，例如 `e2e/`、`src/test/`、`tests/`，以及主要测试框架配置；
- `docs/testing/README.md`、其他重要项目文档和 README；
- Docker / compose、CI、运行与开发入口；
- 能从真实配置中确认的常用 build/test/dev 命令；
- 本次索引对应的 Git HEAD commit SHA，作为新鲜度提示。

如果仓库不在 Git 中，可省略 commit SHA，并说明没有 Git 基准。

## 推荐内容

保持一个 Markdown 文件即可，例如：

```markdown
# SIYRS 项目索引

> 本文件用于快速理解项目结构和定位资料。真实文件始终优先。

索引基准 commit：`abc123...`

## 项目
...

## 模块
### 前端
路径：`web/`
技术：Vue / TypeScript
关键配置：`web/package.json`
测试：`web/e2e/`

## 测试资产
统一入口：`docs/testing/README.md`

## 项目文档
...

## 常用命令
...

## 运行与基础设施
...
```

只写能够从当前仓库确认的事实，不为了模板完整度保留空章节。

## 扫描范围

优先做结构级扫描，不读取所有源码。重点查看根目录、模块目录、构建/测试配置、README、CI 和基础设施入口。

默认忽略生成物和低价值大目录，例如：

- `.git/`
- `node_modules/`
- `target/`
- `dist/`
- `build/`
- `coverage/`
- IDE cache、二进制产物和依赖缓存。

## Secret 边界

可以记录“项目存在 `.env` / secret 配置入口”，但不要把密码、token、API key、cookie、私钥或其他凭证值写入 `.siyrs/README.md`。

发现敏感配置文件时只记录文件路径或环境变量名称中确实有导航价值的部分，并避免复制其值。

## 不复制其他真相源

`.siyrs` 不应该复制：

- 源码正文；
- 测试 Case 正文；
- P0/P1/P2/P3 的完整定义；
- release gate 全文；
- 每次测试结果；
- Git 状态历史。

这些内容分别留在真实代码、`docs/testing/`、CI 或 Git 中；`.siyrs` 只链接过去。

第一版只使用 `.siyrs/README.md`。不要创建 `manifest.json`、`state.json`、`registry.json`、`cache/` 或其他运行时层。

## 什么时候更新

普通代码修改不要求更新项目地图。以下稳定变化发生时，如果 `.siyrs/README.md` 已存在，应同步更新：

- 模块新增、删除或移动；
- 技术栈或主要构建方式变化；
- 测试代码入口或测试框架变化；
- 运行、部署或 CI 主入口变化；
- `docs/testing/` 或其他重要文档入口变化；
- 常用开发/测试命令发生稳定变化。

索引基准 commit SHA 只表示“最近一次项目地图刷新参考了哪个 HEAD”，不是强制 gate，也不意味着这个 commit 之后的所有内容都失效。
