# Research Experiment API

科研实验记录管理后端，当前用于记录实验基本信息，并为后续的实验运行、指标分析和科研 Agent 扩展提供稳定的后端基础。

本项目基于开源 Issue Reporting and Tracking API 重构而来。原始项目保存在同级目录 `original-project`，当前仓库只维护科研实验领域的重构代码。

## 当前状态

当前版本已经完成：

- `Experiment` 模型；
- SQLAlchemy 2.x ORM；
- Alembic 初始迁移；
- Experiment CRUD API；
- Pydantic 输入输出模型分离；
- Repository、Service、API Router 分层；
- SQLite 测试数据库；
- PostgreSQL 本地环境连接和迁移验证；
- pytest Schema、Repository、Service 和 API 测试；
- Docker 镜像构建和 Compose 联调。

## 技术栈

- Python 3.11
- FastAPI
- Pydantic 2
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- pytest
- Docker / Docker Compose
- Uvicorn

## 项目结构

```text
research-experiment-agent/
├── app/
│   ├── api/routes/experiments.py
│   ├── core/config.py
│   ├── db/base.py
│   ├── db/session.py
│   ├── models/experiment.py
│   ├── repositories/experiment.py
│   ├── schemas/experiment.py
│   ├── services/experiment.py
│   └── main.py
├── alembic/
│   ├── versions/
│   └── env.py
├── tests/
│   ├── conftest.py
│   ├── test_experiment_api.py
│   ├── test_experiment_repository.py
│   ├── test_experiment_schema.py
│   └── test_experiment_service.py
├── alembic.ini
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
├── .env.example
└── README.md
```

## 领域模型

当前阶段只实现 `Experiment`，避免一次引入过多业务表。

| 字段 | 说明 |
|---|---|
| `id` | 实验主键 |
| `name` | 实验名称 |
| `description` | 实验描述，可为空 |
| `hypothesis` | 实验假设，可为空 |
| `status` | `planned`、`running`、`completed`、`archived`、`failed` |
| `created_at` | 创建时间 |
| `updated_at` | 更新时间 |

## 环境要求

- Python 3.11；
- Git；
- PostgreSQL，或 Docker Desktop；
- PowerShell、Bash 或其他终端。

Python 3.13 可能触发部分依赖的本地编译问题，因此当前项目固定使用 Python 3.11 虚拟环境。

## 本地安装

在项目根目录执行：

```powershell
python -m venv .venv311
.\\.venv311\\Scripts\\Activate.ps1
python -m pip install -r requirements-dev.txt
```

## 环境变量

复制模板：

```powershell
Copy-Item .env.example .env
```

`.env.example` 只保存变量名称和非敏感示例。`.env` 保存本机真实配置，已加入 `.gitignore`，不要提交或发送其内容。

主要变量：

```env
APP_NAME=Research Experiment API
APP_ENV=development
API_HOST=127.0.0.1
API_PORT=8000
DATABASE_URL=
POSTGRES_DB=research_experiment
POSTGRES_USER=research_experiment
POSTGRES_PASSWORD=
```

使用 PostgreSQL 时，把本机的 `DATABASE_URL` 设置为：

```text
postgresql+psycopg://用户名:本地密码@127.0.0.1:5433/数据库名
```

如果 `DATABASE_URL` 留空，当前开发配置会回退到项目目录下的 SQLite 数据库 `experiment.db`。

不要把真实密码写入 README、日志、提交记录或问题反馈中。

## 数据库迁移

查看当前迁移版本：

```powershell
python -m alembic current
```

执行全部迁移：

```powershell
python -m alembic upgrade head
```

创建新的自动迁移：

```powershell
python -m alembic revision --autogenerate -m "describe your change"
```

迁移前请确认 `DATABASE_URL` 指向本地开发数据库或测试数据库。

## 启动 API

```powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

启动后访问：

- Swagger UI：<http://127.0.0.1:8000/docs>
- ReDoc：<http://127.0.0.1:8000/redoc>
- OpenAPI JSON：<http://127.0.0.1:8000/openapi.json>

## API 接口

| 方法 | 路径 | 说明 | 成功状态码 |
|---|---|---|---|
| POST | `/experiments/` | 创建实验 | `201` |
| GET | `/experiments/` | 查询实验列表，支持 `skip`、`limit` | `200` |
| GET | `/experiments/{experiment_id}` | 查询单个实验 | `200` |
| PATCH | `/experiments/{experiment_id}` | 部分更新实验 | `200` |
| DELETE | `/experiments/{experiment_id}` | 删除实验 | `204` |

创建请求示例：

```json
{
  "name": "Cell culture experiment",
  "description": "Verify the baseline culture condition",
  "hypothesis": "The baseline condition should remain stable",
  "status": "planned"
}
```

部分更新示例：

```json
{
  "name": "Updated experiment",
  "status": "running"
}
```

常见错误：

- `404`：目标实验不存在；
- `422`：请求体或查询参数不符合 Pydantic 校验规则；
- `500`：未处理的服务器异常，应结合日志定位。

## 测试

测试使用独立的内存 SQLite 数据库，不会修改开发数据库。

运行全部测试：

```powershell
python -m pytest -q
```

按测试层运行：

```powershell
python -m pytest -q tests/test_experiment_schema.py
python -m pytest -q tests/test_experiment_repository.py
python -m pytest -q tests/test_experiment_service.py
python -m pytest -q tests/test_experiment_api.py
```

测试覆盖：

- Schema 合法输入、默认值、空格清理和非法输入；
- Repository 创建、查询、列表、分页、更新和删除；
- Service 创建、查询异常、更新和删除；
- API CRUD、404 和 422 响应。

最近一次本地测试记录为全部测试通过，具体结果以当前环境运行输出为准。

## PostgreSQL 本地验证

已经完成以下本地验证：

1. PostgreSQL 容器启动；
2. Alembic 使用 `PostgresqlImpl`；
3. `experiments` 表迁移成功；
4. FastAPI 创建接口成功写入 PostgreSQL；
5. 通过 SQL 查询确认数据已写入 `experiments` 表。

## Docker

仓库中包含：

- `Dockerfile`：构建 FastAPI 应用镜像；
- `docker-compose.yml`：启动 PostgreSQL 和 FastAPI API 服务；
- `.dockerignore`：避免把虚拟环境、`.env` 和测试缓存复制到镜像。

启动完整服务：

```powershell
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

API 容器启动时会先执行 `alembic upgrade head`，再启动 Uvicorn。

服务地址：

- API：<http://127.0.0.1:8000>
- Swagger UI：<http://127.0.0.1:8000/docs>
- PostgreSQL：`127.0.0.1:5433`

当前已验证镜像构建、PostgreSQL 健康检查、Alembic 容器迁移和 API 容器内的 `201 Created` 请求。

## 分层设计

```text
FastAPI Router
    ↓
Service
    ↓
Repository
    ↓
SQLAlchemy Session
    ↓
SQLite / PostgreSQL
```

- Router：处理 HTTP 参数、状态码和错误转换；
- Service：处理业务流程、提交和回滚事务；
- Repository：封装 SQLAlchemy 查询和持久化操作；
- Schema：负责输入校验和 ORM 输出转换；
- Model：描述数据库表结构。

## 后续路线

1. `ExperimentRun` 实验运行记录；
2. `Metric` 实验指标；
3. `Tag` 和实验标签关联；
4. `ExperimentNote` 实验笔记；
5. LLM API；
6. Tool Calling；
7. Agent 循环和工具错误处理；
8. 超时、重试和日志；
9. RAG；
10. SSE 流式输出；
11. Agent 评测；
12. 权限、审计和可靠性设计。

## 安全注意事项

- 不要提交 `.env`；
- 不要在日志和 README 中写数据库密码；
- 不要把真实数据库连接信息写入测试代码；
- 迁移和测试优先使用本地开发数据库或独立测试数据库；
- `original-project` 与当前重构仓库分开保存。
