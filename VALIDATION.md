# 文档与示例核验记录

核验日期：2026-11-21。对象：本仓库规范 1.0.0 的文档、模板、清单与说明性示例。以下结果不代表业务系统已通过测试或已部署。

## 交付清单

| 交付物 | 数量 | 入口 |
| --- | --- | --- |
| 规范正文 | 11 章 | [导航](README.md) |
| 官方参考与维护说明 | 1 份 | [参考资料](docs/references.md) |
| 工作模板 | 16 份 | [技术基线](templates/01-project-baseline.md)至[业务项目 AGENTS.md](templates/16-project-agents.md) |
| 阶段检查清单 | 5 份 | [设计](checklists/01-design.md)至[运维](checklists/05-operations.md) |
| 订单贯穿示例 | 4 份说明＋1 份 OpenAPI | [订单示例](examples/order/README.md) |
| Docker 示例 | 说明、Compose 配置、变量示例 | [Docker 示例](examples/docker/README.md) |
| 根目录文档 | 导航、智能体协作指南、变更记录、本核验记录 | [首页](README.md)、[AGENTS.md](AGENTS.md) |
| 规范接入 skill | 入口、展示配置 | [SKILL.md](SKILL.md)、[配置](agents/openai.yaml) |
| 分发与验证工具 | 打包脚本、7 项自动检查 | [脚本](scripts/package_skill.py)、[检查](tests/test_distribution.py) |

初始交付合计 40 份 Markdown、2 份 YAML 和 1 份环境变量示例，共 43 个文件；新增 `AGENTS.md` 后为 41 份 Markdown、共 44 个文件。强制规则仍为 102 条。

本次增加业务项目模板、skill 与分发工具后，交付为 43 份 Markdown、3 份 YAML、2 份 Python、1 份环境变量示例和 `.gitignore`，共 50 个文件；不含生成物和 Git 元数据。

## 初始交付已执行的核验

| 检查 | 结果与范围 |
| --- | --- |
| 文档编码、代码围栏、表格和本地链接 | UTF-8 可读取，围栏成对，表格列数一致，本地目标存在 |
| 规则编号 | 102 条定义无重复，规则引用均有定义，每条规则至少关联一份阶段检查清单 |
| YAML 格式 | OpenAPI 和 Compose 均可解析，未发现重复键 |
| OpenAPI 结构与引用 | 3 个唯一 operationId，44 处本地引用可解析；路径参数和成功／公共失败响应已检查 |
| OpenAPI 示例约束 | 对已使用的类型、必需字段、枚举常量、模式、范围和格式进行校验，12 个示例通过 |
| 接口负面样例 | 数字型业务 ID、无小数金额、越界数量、小数数量、额外价格字段共 5 类非法输入被约束拒绝 |
| Markdown JSON | 3 个 JSON 代码块解析通过 |
| Java 金额片段 | 从说明文档提取后编译成功；正常金额、精确规范化、零价格、空价格、负价格、数量下界／上界及精度异常共 8 个场景通过 |
| Vue 脚本片段 | 提取 `<script setup>` 内 JavaScript，执行语法检查通过 |
| Docker Compose | 使用变量示例执行 `docker compose --env-file .env.example -f compose.yaml config --quiet`，退出码 0；已修正本机 Compose 不接受带引号 CPU 数值的问题 |

Java、Vue 片段验证使用临时目录，检查结束已自动清理；未向项目引入业务工程或依赖。Compose 检查只解析配置，没有启动容器或下载镜像。

## 核验边界与接入时待完成项

- 当前环境未提供完整 OpenAPI 标准校验器，本次执行 YAML、引用、所用约束与示例校验；不能替代完整规范校验及实际接口契约测试。
- Vue 未安装实际业务依赖，没有执行单文件组件模板编译、浏览器交互、可访问性或端到端测试；相关场景已列入示例验证方案。
- Java 验证仅证明独立金额片段的语法与列出的业务边界，不代表事务、并发、数据库集成或整套阿里巴巴手册检查通过。
- Compose 使用不存在的占位镜像与项目待提供的秘密文件；未验证镜像运行、文件权限、应用配置读取、健康脚本、代理、数据库连接及资源容量。
- 性能、可用性、备份恢复和发布回滚均为规范与待执行方案，没有虚构实测结果。具体项目完成技术选型后执行并提交证据。
- 本次未逐条探测所有外部参考链接的在线可用性；固定手册基线与官方入口已列在参考资料，维护者按周期复核。

## 智能体指南补充核验（2026-11-21）

- 新增 `AGENTS.md`，同步首页入口、变更记录和本核验记录；不改变规范规则及等级。
- 对当前 41 份 Markdown 执行静态检查：UTF-8 可读取，代码围栏闭合，69 个表格列数一致，187 处本地链接目标存在。
- 102 条规则定义无重复；规则引用及编号区间均可解析，每条强制规则仍有关联阶段检查清单。
- 本次未重新执行 Java、Vue、OpenAPI、Compose 或业务运行验证；上方相关结果为初始交付记录，不作为本次新增指南的运行验证结论。

## 业务项目模板与 skill 核验（2026-11-21）

- 变更范围：业务项目 AGENTS.md 模板、根目录 skill 及展示配置、GitHub 安装与使用说明、快照打包脚本、分发测试、导航与记录；规范规则及业务示例内容未修改。
- 环境：Windows、Python 3.10.9、PyYAML 6.0、Git 2.17.1.windows.2。Git 分支查询使用兼容入口，未沿用不支持的 `git branch --show-current` 结果。
- 在仓库根目录运行 `python -X utf8 -m unittest discover -s tests -v`，7 项通过：源码与搬迁后的规范快照逐文件一致，摘要与快照标识匹配；本地链接可解析；已有输出不覆盖；缺失来源不生成输出；拒绝写入规范资料目录；相同输入生成相同 ZIP；无 Git 元数据的 GitHub 根目录安装布局可以生成完整快照。
- Markdown 检查覆盖当前 43 份文档的 UTF-8、围栏、表格列数与本地链接；102 条规则定义无重复，引用及编号区间可解析，每条规则至少关联一份阶段清单。
- 使用本机 Codex 提供的 `skill-creator/scripts/quick_validate.py` 对根目录 skill 校验通过；`git diff --check` 通过。临时打包及搬迁数据由测试在临时目录创建并清理。
- 远端验证：将功能提交 `29c4fce` 推送到 `guoshiqiufeng/easy-standard` 的 `codex/java-vue-standards-skill` 分支后，使用 Codex 自带安装器，按 README 中的 GitHub 仓库、ref、根路径 `.`、名称和 download 方式实际安装到本仓库 `dist/github-install-check/`（未改全局安装）。安装成功；安装后的 skill 格式校验通过，其打包脚本独立生成 ZIP，安装副本内再次执行 7 项检查全部通过。Markdown 实际核验 43 份、72 个表格、204 处本地链接。
- 未在实际业务项目执行完整智能体接入／重复接入／升级，未完成非作者评审，也未重新执行 Java、Vue、OpenAPI、Compose 或业务运行测试；这些范围不能记为通过。远端验证仅证明下载、文件布局、打包与已列检查可执行，不代表业务规范采纳完成。

## main 安装说明更新核验（2026-11-21）

- 同步并确认 GitHub main 已包含合并提交 `a114d4b`。本次仅更新 README 的安装来源说明和两种系统的安装命令，并同步变更、核验记录；规范、skill 逻辑和业务示例未修改。
- 使用本机 Codex 安装器，按 README 的仓库、`--ref main --path . --name java-vue-standards --method download` 参数实际下载到 `dist/github-main-install-check/`，安装成功；安装后的 skill 通过 `quick_validate.py` 校验。下载后远端 main 仍为 `a114d4b9f5ebd68e95188fb69382f359f82f6a59`，未改动全局 skill 安装。
- 在仓库根目录执行 `python -X utf8 -m unittest discover -s tests -v`，7 项通过；43 份 Markdown、72 个表格、204 处本地链接及 102 条规则引用检查通过。`git diff --check` 通过，README 不再引用旧功能分支。
- 本次未在实际业务项目执行接入、升级或运行测试，也未在 macOS／Linux 执行命令；两种系统示例仅将相同安装参数切换到 main。新文档变更尚待独立评审，先前功能分支的核验记录保留为历史证据。

## 接入验收

先完成[技术基线](templates/01-project-baseline.md)，确定工具与版本、强制检查入口、采用的推荐阈值、性能与恢复目标；随后按[设计](checklists/01-design.md)、[合并](checklists/02-merge.md)、[测试](checklists/03-test-acceptance.md)、[发布](checklists/04-release.md)和[运维](checklists/05-operations.md)清单执行。任何实际执行记录应关联真实提交、制品、环境与责任人。
