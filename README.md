# FastAPI Template

基于 FastAPI + async SQLAlchemy 的项目模板，支持 PostgreSQL 和 SQLite，采用分层架构。

## 技术栈

- **框架：** FastAPI
- **ORM：** SQLAlchemy 2.0 (async)
- **数据库：** PostgreSQL (asyncpg) / SQLite (aiosqlite)
- **数据校验：** Pydantic v2
- **配置管理：** pydantic-settings
- **日志：** Loguru
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
│   └── users.py
├── services/                # 业务逻辑层 (校验、编排)
│   └── user_service.py
├── repositories/            # 数据访问层 (静态方法，接收 db session)
│   └── user_repository.py
├── models/                  # SQLAlchemy ORM 模型
│   └── user.py
└── schemas/                 # Pydantic 请求/响应模型
    ├── user.py
    └── response.py          # 统一响应结构 ApiResponse[T]
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

> 开发模式下 (`APP_ENV=development`) 会自动同步表结构，生产环境需手动管理数据库迁移。

## API 接口

所有接口前缀为 `/api`，返回统一的响应结构：

```json
{
  "code": 200,
  "msg": "success",
  "data": {}
}
```

### Users

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/users/` | 创建用户 |
| GET | `/api/users/` | 获取用户列表 (支持 skip/limit 分页) |
| GET | `/api/users/{user_id}` | 获取单个用户 |
| PUT | `/api/users/{user_id}` | 更新用户 |
| DELETE | `/api/users/{user_id}` | 删除用户 |

## 统一响应格式

### 成功响应

```json
{
  "code": 200,
  "msg": "success",
  "data": { "id": 1, "username": "alice", "email": "alice@example.com" }
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

## 开发约定

- 使用 **Tab** 缩进
- 使用绝对路径导入 (如 `from app.core.config import settings`)
- Repository 方法为 `@staticmethod`，第一个参数为 `db: AsyncSession`
- Service 层通过 `BizException` 抛出业务异常，不依赖 FastAPI
- 路由层使用 `ApiResponse[T]` 作为 `response_model`，返回值用 `ApiResponse.ok()` 包裹
