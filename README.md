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
app/
├── main.py                  # 应用入口
├── core/
│   ├── app.py               # 应用工厂 + 生命周期管理
│   ├── config.py            # 配置中心 (pydantic-settings)
│   ├── database.py          # 异步引擎、会话工厂、Base、get_db()
│   └── exceptions.py        # BizException + 全局异常处理器
├── api/                     # 路由层 (薄层，只做请求/响应)
│   ├── users.py             # 用户接口
│   ├── conversations.py     # 会话接口
│   └── messages.py          # 消息接口
├── services/                # 业务逻辑层 (校验、编排)
│   ├── user_service.py
│   ├── conversation_service.py
│   └── message_service.py
├── repositories/            # 数据访问层 (静态方法，接收 db session)
│   ├── user_repository.py
│   ├── conversation_repository.py
│   └── message_repository.py
├── models/                  # SQLAlchemy ORM 模型
│   ├── user.py              # 用户模型
│   ├── conversation.py      # 会话模型
│   └── message.py           # 消息模型
└── schemas/                 # Pydantic 请求/响应模型
    ├── response.py          # 统一响应结构 ApiResponse[T] + PageData[T]
    ├── user.py
    ├── conversation.py
    └── message.py
tests/
├── conftest.py              # 测试配置和 fixtures
├── test_users.py            # 用户接口测试
├── test_conversations.py    # 会话接口测试
└── test_messages.py         # 消息接口测试
```

## 架构

```
API (路由层)  →  Service (业务层)  →  Repository (数据层)  →  Database
```

- **路由层**只负责接收请求、返回响应，不包含业务逻辑
- **业务层**处理校验和业务规则，抛出 `BizException`
- **数据层**封装所有数据库操作，方法均为 `@staticmethod`
- 所有数据库操作均为异步

## 快速开始

### 安装依赖

```bash
uv sync
```

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

以 Users 为例，其余资源（Conversations、Messages）遵循相同的 RESTful 风格：

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users/` | 创建用户 |
| GET | `/api/users/` | 获取用户列表 (分页) |
| GET | `/api/users/{user_id}` | 获取单个用户 |
| PUT | `/api/users/{user_id}` | 更新用户 |
| DELETE | `/api/users/{user_id}` | 删除用户 |

完整接口文档启动后访问 `/docs` 查看。

## 统一响应格式

所有接口返回统一的 `ApiResponse[T]` 结构：

### 成功响应

```json
{
  "code": 200,
  "msg": "success",
  "data": { "id": 1, "username": "alice", "email": "alice@example.com" }
}
```

### 分页响应

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "list": [{ "id": 1, "username": "alice", "email": "alice@example.com" }],
    "total": 50,
    "page": 1,
    "page_size": 20
  }
}
```

### 业务异常

```json
{
  "code": 404,
  "msg": "User not found",
  "data": null
}
```

### 参数校验错误

```json
{
  "code": 422,
  "msg": "Validation error",
  "data": [{ "loc": ["body", "username"], "msg": "Field required", "type": "missing" }]
}
```

### 服务器错误

```json
{
  "code": 500,
  "msg": "Internal server error",
  "data": null
}
```

## 数据模型

以 Conversation 为例：

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | str | 用户标识 |
| title | str | 会话标题 |
| model_name | str | 模型名称 |
| extra_data | JSON | 扩展数据 (模型配置等) |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

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

**详细说明：** 查看 [tests/README.md](tests/README.md) 了解更多测试命令和配置说明。

## 代码质量

### 代码格式化和检查

项目使用 **Ruff** 进行代码格式化和 linting（采用温和规则，易于团队协作）：

```bash
# 检查代码质量
uv run ruff check app/

# 自动修复问题
uv run ruff check app/ --fix

# 格式化代码
uv run ruff format app/
```

### Ruff 配置说明

- **行长度：** 120 字符
- **缩进风格：** Tab（4 个空格宽度）
- **启用规则：**
  - `E` - pycodestyle 错误（语法错误、明显问题）
  - `F` - pyflakes（未使用的导入、未定义的变量）
  - `I` - isort（导入排序）
- **设计理念：** 只检查真正的错误，不强制过于严格的风格规范

### VSCode 集成（推荐）

项目已配置 VSCode 设置（`.vscode/settings.json`），安装 Ruff 扩展后：

✅ **自动功能（保存时）：**
- 代码格式化
- 导入排序和清理
- 删除未使用的导入

⚠️ **提示警告（需手动修复）：**
- 未定义的变量
- 语法错误
- 重复导入

**安装扩展：**
```bash
# VSCode 会自动提示安装推荐扩展，或手动安装：
code --install-extension charliermarsh.ruff
```

**详细说明：** 查看 [.vscode/README.md](.vscode/README.md) 了解 VSCode 中的 Ruff 使用指南。

**建议：** 提交代码前运行 `ruff check` 确保代码质量。

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
- Repository 方法为 `@staticmethod`，第一个参数为 `db: AsyncSession`
- Service 层通过 `BizException` 抛出业务异常，不依赖 FastAPI
- 路由层使用 `ApiResponse[T]` 作为 `response_model`，返回值用 `ApiResponse.ok()` 包裹
- 提交代码前运行 `ruff check --fix` 和 `ruff format` 确保代码质量
