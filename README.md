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
