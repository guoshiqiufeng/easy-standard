# Java＋Vue 3 团队项目规范

版本：1.0.0 · 制定日期：2026-11-21 · 状态：可供团队评审、采纳

适用于常规企业 Web 业务，覆盖需求、设计、开发、测试、发布、运维和退役。默认采用模块化单体、Java 后端、Vue 3 前端、Linux＋Docker 部署。Java 遵循阿里巴巴《Java 开发手册（黄山版）》；其余技术栈由项目登记选择。本仓库提供文档与模板，不包含可运行的业务脚手架。

## 如何开始

使用智能体协作时，先阅读 [AGENTS.md](AGENTS.md)，按任务查阅对应规范、模板与检查清单。

1. 项目负责人复制[技术基线模板](templates/01-project-baseline.md)，登记技术版本、角色、质量门槛、性能与恢复目标。
2. 需求与设计阶段填写[需求](templates/02-requirements.md)、[系统设计](templates/03-system-design.md)、[架构决策](templates/04-adr.md)、[接口](templates/05-api-contract.md)和[数据变更](templates/06-data-change.md)。
3. 按开发规范实现；使用[代码评审模板](templates/07-code-review.md)及[合并检查清单](checklists/02-merge.md)。
4. 提交[测试计划](templates/08-test-plan.md)、[测试用例](templates/09-test-cases.md)和[测试报告](templates/10-test-report.md)。
5. 上线前准备[发布与回滚方案](templates/11-release.md)、[运维手册](templates/12-runbook.md)、[恢复演练](templates/13-recovery-drill.md)，执行[发布检查](checklists/04-release.md)。
6. 运行阶段执行[运维检查](checklists/05-operations.md)，按需填写[故障复盘](templates/14-incident-review.md)和[规范例外](templates/15-exception.md)。

将模板复制到业务项目文档目录后填写；本仓库保留通用模板。模板中“待填写”是提示，完成的项目文档不得保留无解释的空项；不适用项需说明理由。

## 在其他项目中安装与使用

**推荐通过 GitHub 链接安装 skill，再由 skill 为业务项目生成适配后的 AGENTS.md。** 本仓库根目录的 AGENTS.md 用于维护规范仓库，不能原样复制到业务项目；业务项目使用[专用模板](templates/16-project-agents.md)。[SKILL.md](SKILL.md) 位于仓库根目录，安装时需要同时取得规范、模板、清单和示例。

### 通过 GitHub 链接安装

GitHub 仓库：[guoshiqiufeng/easy-standard](https://github.com/guoshiqiufeng/easy-standard)。本次功能提交在 `codex/java-vue-standards-skill` 分支；合并前使用该分支安装，合并后可选择 `main` 或经过评审的固定提交。

在 Codex 中直接发送下面这段话：

```text
请使用 skill-installer 从 GitHub 安装这个 skill：
https://github.com/guoshiqiufeng/easy-standard

分支：codex/java-vue-standards-skill
skill 路径：仓库根目录（.）
安装名称：java-vue-standards
请安装完整目录，保留 docs、templates、checklists、examples 和 scripts。
```

也可以调用 Codex 自带的安装脚本。在默认安装目录下，PowerShell 示例为：

```powershell
python "$env:USERPROFILE/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" --repo guoshiqiufeng/easy-standard --ref codex/java-vue-standards-skill --path . --name java-vue-standards --method download
```

macOS／Linux 示例为：

```sh
python3 ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo guoshiqiufeng/easy-standard --ref codex/java-vue-standards-skill --path . --name java-vue-standards --method download
```

命令中的脚本路径以实际 Codex 安装位置为准；设置了 `CODEX_HOME` 时使用该目录下的 `skills/.system/skill-installer/scripts/install-skill-from-github.py`。安装器通常放入 `$CODEX_HOME/skills/java-vue-standards`，未设置时为 `~/.codex/skills/java-vue-standards`；已有同名目录时先比较并保留定制，不强制覆盖。私有仓库需要有读取权限。使用 `--ref` 指定完整提交 SHA 可固定安装内容；分支名可能随提交变化。

安装后在下一轮目标项目会话中确认能发现 `$java-vue-standards`；未发现时重新启动会话。安装不会自动改写业务项目，首次使用仍需发起接入任务。

### 在业务项目中使用

打开目标业务项目，首次接入时输入：

```text
使用 $java-vue-standards 将团队规范接入当前项目。
保留已有 AGENTS.md 和项目约定，核实技术栈、目录与执行命令。
生成或更新项目指导、技术基线草稿和接入记录，列出冲突与未确认项。
```

默认建议形成下面的结构，已有项目沿用原文档路径：

```text
业务项目/
  AGENTS.md                       项目定位、实际目录、命令与日常约束
  docs/project-baseline.md         技术与质量基线
  docs/standards-adoption.md       来源、差距、冲突、未确认项和验证记录
  standards/team/                  固定版本规范副本及 SNAPSHOT.json
```

skill 按真实项目适配[业务项目版 AGENTS.md 模板](templates/16-project-agents.md)，与现有约定按主题合并，不重复追加。规范副本保持原目录结构，项目文档引用项目内路径，不依赖维护者电脑的绝对路径。日常开发由项目 AGENTS.md 提供持续指导，无需每次重新接入。

只检查当前改动时输入：

```text
使用 $java-vue-standards，按项目已登记的规范版本检查本次未提交改动。
给出规则编号、证据、影响、未验证项和整改建议；本次只检查。
```

升级规范时明确指定目标版本或快照，先比较兼容影响再更新基线。安装新版 skill 不等于业务项目已经同意升级。未知信息写明原因、影响和负责角色，接入状态保持草稿；生成文档与静态检查不能代替负责人采纳、独立评审或业务验收。

### 快照与人工接入

安装目录或本仓库中的[打包脚本](scripts/package_skill.py)用于生成可移动的规范快照，仅依赖 Python 3.10 或更高版本。在该目录执行：

```sh
python scripts/package_skill.py --output dist/java-vue-standards.zip
```

将 ZIP 内的 `java-vue-standards/references/standard/` 复制到业务项目的 `standards/team/`。ZIP 也可用于离线分发整个 skill。脚本不会覆盖已有输出，可另选文件名；`dist/` 不提交 Git。通用模板仍保持通用，填写后的项目文档另外存放。

`SNAPSHOT.json` 登记规范版本、可获得的源提交、未提交状态、逐文件 SHA-256 与快照标识。GitHub 下载目录未保留 Git 信息时，提交和未提交状态为 `null`，接入记录补充实际安装来源与已知 ref，不能猜测提交。摘要用于核对内容完整性，不代表已评审或来源签名。

不使用 skill 时，也可按上述方式准备规范副本，手工适配模板并填写[技术基线](templates/01-project-baseline.md)。规则仍按强制、推荐、可选区分，已有约定与适用强制项冲突时按 `GOV-004` 记录和处理，不默默覆盖。

## 规范导航

| 文档 | 内容 | 首要读者 |
| --- | --- | --- |
| [00 总则与治理](docs/00-governance.md) | 规则等级、职责、交付产物、例外、版本、存量接入 | 全员 |
| [01 需求与系统设计](docs/01-system-design.md) | 模块、分层、容量、非功能目标、架构演进 | 产品、技术负责人 |
| [02 Java 开发](docs/02-java.md) | 阿里巴巴规范映射、编码、异常、并发、事务 | 后端、评审人 |
| [03 Vue 3 开发](docs/03-vue.md) | 组件、状态、请求、表单、安全、体验 | 前端、评审人 |
| [04 接口契约](docs/04-api.md) | REST、响应、错误、分页、幂等、兼容性 | 前后端、测试 |
| [05 数据规范](docs/05-data.md) | 模型、约束、查询、缓存、迁移、生命周期 | 后端、数据负责人 |
| [06 安全规范](docs/06-security.md) | 认证、授权、注入、密钥、审计、漏洞 | 开发、安全、运维 |
| [07 测试与质量](docs/07-testing.md) | 测试层次、场景、缺陷、质量门槛 | 开发、测试 |
| [08 协作与代码评审](docs/08-collaboration.md) | Git、提交、评审、文档、完成定义 | 全员 |
| [09 构建与发布](docs/09-delivery.md) | 流水线、制品、Docker、迁移、回滚 | 开发、运维 |
| [10 运维与可靠性](docs/10-operations.md) | 监控、告警、容量、备份、故障、退役 | 运维、技术负责人 |
| [参考资料与维护说明](docs/references.md) | 官方来源、版本基线、工具兼容性 | 规范维护者 |

## 规则和示例的含义

- **强制**：适用时必须满足；未满足须完成整改或取得有效例外。强制规则使用稳定编号，如 `API-003`。
- **推荐**：默认实践；项目可记录理由后调整。推荐项一经纳入项目质量基线，就按该项目基线检查。
- **可选**：满足特定规模、收益或业务条件后采用。
- 表格“适用”定义边界；“检查与证据”用于验收；“责任”是落实负责人，评审人按流程独立确认。
- 本仓库的接口字段、分页限制、覆盖率建议等属于团队约定，不宣称是外部标准的强制要求。

[订单贯穿示例](examples/order/README.md)连接需求、设计、接口、数据、Java／Vue 3 示例、测试和发布；[Docker 示例](examples/docker/README.md)展示配置边界。示例值不是所有项目的容量承诺，使用前必须完成技术基线登记。

## 评审入口

| 阶段 | 清单 | 通过条件 |
| --- | --- | --- |
| 设计 | [设计评审](checklists/01-design.md) | 需求、方案、契约、数据和风险有结论 |
| 合并 | [代码合并](checklists/02-merge.md) | 自动检查和独立评审通过 |
| 测试 | [测试验收](checklists/03-test-acceptance.md) | 关键场景通过，缺陷与证据完整 |
| 发布 | [生产发布](checklists/04-release.md) | 制品、迁移、回滚、监控和责任人就绪 |
| 运行 | [日常运维](checklists/05-operations.md) | 告警、备份、容量、演练有记录 |

规范变更见 [CHANGELOG](CHANGELOG.md)。本次静态核验结果及未执行的运行验证见 [VALIDATION](VALIDATION.md)。
