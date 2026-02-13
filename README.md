# FastAPI Template

基于 FastAPI + async SQLAlchemy 的项目模板，支持 PostgreSQL 和 SQLite，采用分层架构。

## 技术栈

- **框架：** FastAPI
- **ORM：** SQLAlchemy 2.0 (async)
- **数据库：** PostgreSQL (asyncpg) / SQLite (aiosqlite)
- **数据校验：** Pydantic v2
- **配置管理：** pydantic-settings
- **日志：** Loguru
- **测试：** pytest + pytest-asyncio + httpx
- **包管理：** uv
- **Python：** >= 3.14

## 项目结构

```
├── app/
│   ├── main.py              # 应用入口
│   ├── core/                # 核心模块 (配置、数据库、异常、日志)
│   ├── api/                 # 路由层 (薄层，只做请求/响应)
│   ├── services/            # 业务逻辑层 (校验、编排)
│   ├── repositories/        # 数据访问层 (通用 CRUD 基类 + 各模块)
│   ├── models/              # SQLAlchemy ORM 模型
│   └── schemas/             # Pydantic 请求/响应模型
├── tests/                   # 测试 (pytest + httpx 异步集成测试)
├── alembic/                 # 数据库迁移脚本
├── Dockerfile               # Docker 镜像构建
├── docker-compose.yml       # Docker Compose 编排
├── pyproject.toml           # 项目依赖和工具配置
└── .env.example             # 环境变量示例
```

## 架构

```
API (路由层)  →  Service (业务层)  →  Repository (数据层)  →  Database
```

- **路由层**只负责接收请求、返回响应，不包含业务逻辑
- **业务层**处理校验和业务规则，抛出 `BizException`
- **数据层**封装所有数据库操作，方法均为 `@classmethod`
- 所有数据库操作均为异步

## 快速开始

### 安装依赖

```bash
uv sync
```

### 安装 Git Hooks（可选但推荐）

安装 pre-commit hooks，提交代码前自动检查格式：

```bash
uv run pre-commit install
```

首次提交会稍慢（下载 hooks），之后每次提交约 2-3 秒。

### 配置环境变量

复制 `.env.example` 为 `.env` 并根据需要修改：

```bash
cp .env.example .env
```

主要配置项：

```env
# 应用配置
APP_ENV=development
APP_TITLE=FastAPI Project
DEBUG=True

# 数据库配置 — 切换 DB_ENGINE 即可切换数据库
DB_ENGINE=sqlite          # sqlite | postgres
DB_NAME=fastapi_db

# 日志配置
LOG_LEVEL=INFO
LOG_FILE_ENABLED=True
LOG_FILE_ROTATION=1 day
LOG_FILE_RETENTION=7 days
```

**⚠️ 重要：** `.env` 文件包含敏感信息，已被 `.gitignore` 排除，切勿提交到 Git 仓库。

### 初始化数据库

首次运行需要执行数据库迁移：

```bash
uv run alembic upgrade head
```

### 启动开发服务器

```bash
fastapi dev app/main.py
```

启动后访问 `http://127.0.0.1:8000/docs` 查看交互式 API 文档。

## API 接口

所有接口前缀为 `/api`，返回统一的响应结构。列表接口均支持 `page` / `page_size` 分页，并返回分页元数据。

### Users

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users/` | 创建用户 |
| GET | `/api/users/` | 获取用户列表 (分页) |
| GET | `/api/users/{user_id}` | 获取单个用户 |
| PUT | `/api/users/{user_id}` | 更新用户 |
| DELETE | `/api/users/{user_id}` | 删除用户 |

### Conversations

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/conversations/` | 创建会话 |
| GET | `/api/conversations/` | 获取会话列表 (分页，可按 `user_id` 过滤) |
| GET | `/api/conversations/{conversation_id}` | 获取单个会话 |
| PUT | `/api/conversations/{conversation_id}` | 更新会话 |
| DELETE | `/api/conversations/{conversation_id}` | 删除会话（级联删除消息） |

### Messages

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/messages/` | 创建消息 |
| GET | `/api/messages/conversation/{conversation_id}` | 获取会话的消息列表 (分页) |
| GET | `/api/messages/{message_id}` | 获取单条消息 |
| PUT | `/api/messages/{message_id}` | 更新消息 |
| DELETE | `/api/messages/{message_id}` | 删除消息 |

完整接口文档启动后访问 `/docs` 查看。

## 统一响应格式

所有接口返回统一的 `ApiResponse[T]` 结构：

**成功响应：**

```json
{ "code": 200, "msg": "success", "data": { "id": 1, "username": "alice" } }
```

**分页响应：**

```json
{ "code": 200, "msg": "success", "data": { "list": [], "total": 50, "page": 1, "page_size": 20 } }
```

**异常响应：**

```json
{ "code": 404, "msg": "User not found", "data": null }
```

## 数据模型

### User

| 字段 | 类型 | 说明 |
|------|------|------|
| id | int | 主键，自增 |
| username | str | 用户名，唯一 |
| email | str | 邮箱，唯一 |

### Conversation

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | str | 用户标识 |
| title | str | 会话标题 |
| model_name | str | 模型名称 |
| extra_data | JSON | 扩展数据 (模型配置等) |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

### Message

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| conversation_id | UUID | 所属会话 ID (外键，级联删除) |
| role | str | 消息角色：system / user / assistant |
| content | str | 消息内容 |
| status | str | 消息状态：processing / success / error |
| extra_data | JSON | 扩展数据 (思考过程、token 用量等) |
| created_at | datetime | 创建时间 |

## Docker 部署

```bash
# 构建并启动（应用 + PostgreSQL）
docker compose up --build -d

# 查看日志
docker compose logs -f app

# 停止并清理
docker compose down -v
```

## 数据库迁移

项目使用 Alembic 管理数据库 schema 变更。

### 常用命令

```bash
# 初始化/更新数据库
uv run alembic upgrade head

# 生成迁移（修改模型后）
uv run alembic revision --autogenerate -m "描述"

# 回滚最近一次
uv run alembic downgrade -1
```

### 基本流程

```bash
# 1. 修改模型文件（例如 app/models/user.py）
# 2. 生成迁移脚本
uv run alembic revision --autogenerate -m "Add avatar field"

# 3. 检查生成的文件
cat alembic/versions/xxxxx_add_avatar_field.py

# 4. 应用迁移
uv run alembic upgrade head
```

**⚠️ 重要：** 添加新模型时必须在 `alembic/env.py` 中导入，否则 autogenerate 无法检测到。

**详细说明：** 查看 [alembic/README](alembic/README) 了解更多迁移场景和最佳实践。

**Docker 部署：** 容器启动时会自动运行 `alembic upgrade head`。

## 测试

项目包含完整的 API 集成测试，使用 pytest + httpx 进行异步测试，每个测试使用独立的内存 SQLite 数据库确保隔离。

```bash
# 运行所有测试
uv run pytest

# 运行指定文件的测试
uv run pytest tests/test_users.py

# 显示详细输出
uv run pytest -v
```


## 代码质量

项目使用 **Ruff** 进行代码格式化和 linting，并通过 **pre-commit** 在提交时自动检查。

```bash
uv run ruff check app/ --fix   # 检查并自动修复
uv run ruff format app/         # 格式化代码
uv run pre-commit install       # 安装 Git Hooks（首次）
```

**Ruff 配置：**

- **行长度：** 120 字符
- **缩进风格：** Tab（4 个空格宽度）
- **检查规则：**
  - `E` - pycodestyle 错误（基础代码风格）
  - `F` - pyflakes（未使用导入、未定义变量等）
  - `I` - isort（导入排序）

VSCode 用户安装 [Ruff 扩展](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff) 后可在保存时自动格式化，详见 [.vscode/README.md](.vscode/README.md)。

## 日志系统

项目使用 **Loguru** 进行日志管理，配置文件在 `app/core/logging.py`。

### 日志输出

- **控制台输出：** 彩色格式化，便于开发调试
- **文件输出：** 保存在 `logs/app.log`，按天轮转，压缩存储

### 日志配置

通过环境变量控制日志行为：

```env
LOG_LEVEL=INFO              # 日志级别：DEBUG, INFO, WARNING, ERROR
LOG_FILE_ENABLED=True       # 是否启用文件日志
LOG_FILE_ROTATION=1 day     # 日志轮转周期
LOG_FILE_RETENTION=7 days   # 日志保留时间
```

### 使用示例

```python
from loguru import logger

logger.info("User created successfully", user_id=123)
logger.error("Failed to connect to database", error=str(e))
logger.debug("Processing request", data=request_data)
```

## 开发约定

- 使用 **Tab** 缩进
- 使用绝对路径导入 (如 `from app.core.config import settings`)
- Repository 方法为 `@classmethod`，参数为 `cls` + `db: AsyncSession`
- Service 层通过 `BizException` 抛出业务异常，不依赖 FastAPI
- 路由层使用 `ApiResponse[T]` 作为 `response_model`，返回值用 `ApiResponse.ok()` 包裹
- 提交代码前运行 `ruff check --fix` 和 `ruff format` 确保代码质量
