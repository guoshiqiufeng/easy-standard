# 参考资料与版本维护

[返回首页](../README.md)

编写基准日期：2026-11-21。下面链接指向官方来源；线上内容可能变化，本仓库不宣称锁定“最新版本”。采纳项目应登记实际使用的手册、工具和依赖版本，并复核适用性。

| 来源 | 用途与边界 |
| --- | --- |
| [Alibaba P3C 官方仓库](https://github.com/alibaba/p3c) | Java 开发手册和部分自动检查能力；团队固定使用黄山版（2022-02-03）为手册基线，不直接追随仓库主分支变化 |
| [Vue 3 文档](https://vuejs.org/guide/introduction.html) | Vue 3 组件、响应式与应用开发机制 |
| [Vue script setup](https://vuejs.org/api/sfc-script-setup.html) | 单文件组件使用 Composition API 的推荐语法；不强制 TypeScript |
| [Vue 安全指南](https://vuejs.org/guide/best-practices/security.html) | 模板、HTML 和客户端安全边界 |
| [OpenAPI 3.1.0](https://spec.openapis.org/oas/v3.1.0.html) | 接口描述格式；具体业务码、包装和分页为团队自定 |
| [HTTP Semantics RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | HTTP 方法、状态和语义；本规范在其上约定团队用法 |
| [Docker Compose 生产使用](https://docs.docker.com/compose/how-tos/production/) | 生产与开发配置区分、部署考虑 |
| [Compose 服务配置](https://docs.docker.com/reference/compose-file/services/) | 健康检查、权限、资源、重启及服务配置；需验证实际 Compose 版本支持 |
| [Docker secrets](https://docs.docker.com/compose/how-tos/use-secrets/) | 受控文件注入示例；Compose 本地文件不等于托管加密密钥服务 |
| [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/) | 安全验证主题参考；项目须登记采用的具体版本、范围与级别，不默认视为认证通过 |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | 认证、授权、输入输出、日志和秘密管理实践 |

## 维护流程

1. 规范维护者核对官方来源的版本和变更，避免将草案、旧工具能力或第三方转载作为强制依据。
2. 涉及新 JDK、Vue、数据库、容器或工具时，在候选技术栈中验证兼容性，保留执行记录。
3. 更新规则、对应模板、检查清单和贯穿示例，检查交叉引用与默认值一致。
4. 按治理规范记录版本、迁移期和通知，项目选择升级并更新技术基线。

不在仓库复制完整第三方手册。团队约定与外部标准保持明确区分，P3C 检查通过不等于所有手册条款通过。
