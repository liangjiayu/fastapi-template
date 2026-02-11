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

复制 `.env` 文件并根据需要修改：

```env
# 应用配置
APP_ENV=development
APP_TITLE=FastAPI Project
APP_DESCRIPTION=A modern FastAPI project structure
DEBUG=True

# 数据库配置 — 切换 DB_ENGINE 即可切换数据库
DB_ENGINE=sqlite          # sqlite | postgres
DB_NAME=fastapi_db
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=
```

### 启动开发服务器

```bash
fastapi dev app/main.py
```

启动后访问 `http://127.0.0.1:8000/docs` 查看交互式 API 文档。

> **SQLite 模式：** 开发环境下会自动创建表结构，无需额外操作。
>
> **PostgreSQL 模式：** 需使用 `sql/schema.sql` 手动创建表结构。

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

以 Conversation 为例，完整建表语句见 `sql/schema.sql`：

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

首次启动时 PostgreSQL 会自动执行 `sql/schema.sql` 完成建表。

## 测试

项目包含完整的 API 集成测试，覆盖所有接口的 CRUD 操作和业务规则校验。

### 运行测试

```bash
# 运行所有测试
uv run pytest tests/ -v

# 运行指定模块测试
uv run pytest tests/test_users.py -v

# 运行单个测试函数
uv run pytest tests/test_users.py::test_create_user -v
```

### 测试覆盖

- **Users API** (7 个测试) - 创建、获取、列表、更新、删除 + 用户名唯一性校验 + 404 错误
- **Conversations API** (7 个测试) - 创建、获取、列表、user_id 过滤、更新、删除 + 404 错误
- **Messages API** (7 个测试) - 创建、获取、列表、更新、删除 + conversation 存在性校验 + 404 错误

**共 21 个测试用例**，涵盖所有 API 端点的正常流程和关键业务规则。

### 测试基础设施

- 使用 **内存 SQLite 数据库** (`sqlite+aiosqlite:///`) 进行测试隔离
- 通过 **httpx AsyncClient** 进行集成测试，直接调用 ASGI 应用
- 每个测试前自动建表，测试后自动删表，确保完全隔离
- 测试依赖：`pytest`、`pytest-asyncio`、`httpx`

## 开发约定

- 使用 **Tab** 缩进
- 使用绝对路径导入 (如 `from app.core.config import settings`)
- Repository 方法为 `@staticmethod`，第一个参数为 `db: AsyncSession`
- Service 层通过 `BizException` 抛出业务异常，不依赖 FastAPI
- 路由层使用 `ApiResponse[T]` 作为 `response_model`，返回值用 `ApiResponse.ok()` 包裹
