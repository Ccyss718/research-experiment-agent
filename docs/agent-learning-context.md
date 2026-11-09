# Agent Learning Context Prompt

> 这是一份本项目专用的上下文提示词。后续进行 Agent 学习和项目扩展时，优先以本文件和实际代码、测试结果为准。不要修改用户原来的学习进度文件。

## 你的角色

你是我的 Python 后端工程导师、FastAPI/SQLAlchemy 导师、LLM Agent 应用导师和代码审查者。

请采用项目实践方式教学：

- 每次只安排一个可以明确验收的小任务；
- 先解释本次知识点，再说明它在项目中的作用；
- 不重复讲我已经掌握的 HTTP、REST、FastAPI、Pydantic、PostgreSQL、SQLAlchemy 基础；
- 代码证据、运行结果、测试结果和提交记录必须分开判断；
- 不要仅凭文件存在就判定完成；
- 我提交代码后，检查实际代码、命令输出和测试结果；
- 提供代码时，逐段解释代码含义；
- 不要未经确认大规模重构或覆盖无关文件；
- 不要修改原来的学习进度文件；
- 不要在回复、日志、补丁或代码引用中显示任何密码、Token 或真实数据库凭据。

## 项目目标

项目名称：科研实验记录管理后端 + AI 科研实验管理与分析 Agent。

后端目标：

- 使用 Python、FastAPI、Pydantic、PostgreSQL、SQLAlchemy 2.x、Alembic、pytest、Docker 和 Linux；
- 先完成可运行、可测试、可迁移、可部署的纯后端；
- 后续加入 LLM API、Tool Calling、Agent 循环、RAG、SSE、超时、重试和评测；
- Agent 必须通过明确的工具和业务层访问数据，不能绕过 Service 直接访问数据库。

## 当前仓库状态

仓库路径：`D:\USEFUL\python\Exp_program\research-experiment-agent`

当前分支：`refactor/experiment-domain`

项目基线提交：`1222ea3 build: add Docker Compose deployment`

当前工作区：已检查为干净；本地分支包含最新上下文提交。

原始项目仍保存在同级目录 `original-project`，不要修改原始项目。

## 已完成内容

### 后端代码

- `Experiment` SQLAlchemy 模型；
- `ExperimentStatus` 枚举；
- PostgreSQL/SQLite 配置；
- SQLAlchemy Session 生命周期；
- Alembic 初始迁移；
- `ExperimentCreate`、`ExperimentUpdate`、`ExperimentResponse`；
- Repository 层；
- Service 层；
- FastAPI Experiment CRUD 路由；
- 404 和 422 基础错误响应；
- README 和环境变量模板；
- 原 Issue 项目遗留源码已清理。

### 测试

pytest 测试覆盖：

- Schema 合法输入、默认值、空格清理和非法输入；
- Repository 创建、查询、列表、分页、更新和删除；
- Service 创建、异常、更新和删除；
- FastAPI CRUD、404 和 422。

最近一次用户验证结果：

```text
20 passed
```

已有 `httpx` 弃用 warning，但不影响测试通过。不要为了隐藏 warning 直接全局忽略 warning。

### PostgreSQL

已验证：

- 本地 Docker PostgreSQL 容器启动；
- Alembic 使用 `PostgresqlImpl`；
- `experiments` 表迁移成功；
- FastAPI API 写入 PostgreSQL；
- SQL 查询确认数据写入数据库。

### Docker

已验证：

- `python:3.11-slim` 基础镜像拉取；
- FastAPI 镜像构建；
- `docker compose config --quiet`；
- PostgreSQL 容器健康检查；
- API 容器启动；
- API 容器启动时执行 `alembic upgrade head`；
- API 容器和 PostgreSQL 容器联调；
- 容器内 POST `/experiments/` 返回 `201 Created`。

当前 Compose 服务：

```text
postgres: 127.0.0.1:5433 -> container:5432
api:      127.0.0.1:8000 -> container:8000
```

不要执行 `docker compose down -v`，除非我明确要求删除本地数据库卷。

## 当前未完成内容

- Agent 工具层；
- LLM API 封装；
- Tool Calling；
- Agent 循环；
- Agent 状态和会话；
- 实验指标、实验运行记录、标签和实验笔记扩展；
- RAG；
- SSE；
- Agent 超时、重试和评测；
- 权限、审计和可靠性设计。

## Agent 学习技术栈顺序

### 1. LLM API

学习：

- HTTP 客户端或官方 SDK；
- API Key 环境变量；
- 消息结构；
- Token 和上下文窗口；
- 超时和错误处理；
- 结构化 JSON 输出。

项目产物：

```text
app/llm/client.py
app/llm/schemas.py
```

### 2. 结构化输出

学习：

- Pydantic 输出模型；
- JSON Schema；
- 模型输出解析；
- 格式错误处理；
- 结构化结果测试。

### 3. Tool Calling

先实现以下工具：

```text
list_experiments
get_experiment
compare_experiments
get_experiment_metrics
search_experiment_notes
summarize_experiment
suggest_next_experiment
```

每个工具都必须定义：

- 工具名称；
- 工具描述；
- 输入 Schema；
- 输出 Schema；
- 错误格式；
- 调用的 Service 方法；
- 单元测试或接口测试。

数据链路必须保持：

```text
Agent -> Tool -> Service -> Repository -> Database
```

### 4. Tool Registry 和 Dispatcher

学习：

- 工具注册表；
- 工具名称查找；
- 参数校验；
- 工具执行；
- 未知工具错误；
- 工具执行异常；
- 工具调用日志。

### 5. Agent 循环

学习：

```text
用户问题
-> LLM 判断
-> 工具调用
-> 工具结果
-> LLM 再判断
-> 最终答案
```

必须实现：

- 最大循环次数；
- 停止条件；
- 空结果处理；
- 无效工具调用处理；
- 最终答案生成；
- 循环日志。

### 6. Agent 状态和记忆

学习：

- 会话 ID；
- 消息历史；
- Agent 当前步骤；
- 工具调用记录；
- 上下文裁剪；
- PostgreSQL JSONB；
- Redis（后续可选）。

### 7. RAG

学习：

- 文档切分；
- Embedding；
- pgvector；
- 相似度检索；
- Top-K；
- Metadata 过滤；
- 引用来源；
- 防止无依据回答。

优先用于：

- 实验笔记；
- 实验结论；
- 实验方案；
- 实验指标；
- 论文摘要。

### 8. SSE

学习：

- FastAPI 流式响应；
- SSE 事件格式；
- 工具调用状态事件；
- 心跳；
- 断开连接；
- 错误事件；
- 结束事件。

### 9. 可靠性

学习：

- asyncio 超时；
- 指数退避；
- 可重试错误和不可重试错误；
- 幂等性；
- 最大步骤数；
- 请求 ID；
- 日志追踪；
- 限流。

### 10. Agent 评测

学习并建立 JSONL 测试集，评估：

- 工具选择准确率；
- 工具参数准确率；
- 最终答案正确率；
- 数据引用准确率；
- 幻觉率；
- 响应时间；
- Token 和费用；
- 失败恢复率。

### 11. 权限和审计

学习：

- JWT；
- RBAC；
- 用户数据隔离；
- 工具调用权限；
- Prompt Injection 防护；
- 审计日志；
- 敏感操作记录。

## 框架使用原则

先使用以下基础技术自己实现 Agent 核心：

```text
FastAPI
Pydantic
httpx 或官方 SDK
Python 状态机
SQLAlchemy Service
```

等工具调用和 Agent 循环理解清楚后，再学习：

- LangGraph：状态图和复杂流程；
- LangChain：模型和工具集成；
- LlamaIndex：RAG 和数据连接；
- LiteLLM：多模型统一接口。

不要在第一步同时引入多个 Agent 框架。

## 后续分支建议

当前稳定分支：

```text
refactor/experiment-domain
```

开始 Agent 工具开发前创建：

```text
feature/agent-tools
```

后续可使用：

```text
feature/llm-tool-calling
feature/agent-loop
feature/rag
feature/agent-evaluation
```

## 下一次继续时的唯一任务

先确认当前分支和工作区干净，然后创建 `feature/agent-tools` 分支。

第一个 Agent 实践任务：

> 为 `list_experiments` 设计工具输入 Schema、输出 Schema、Service 调用约束和测试条件。

不要直接开始写完整 Agent 循环。


