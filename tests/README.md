# 测试说明

## 概述

使用 pytest + httpx 进行异步 API 测试，每个测试使用独立的内存 SQLite 数据库，确保测试隔离。

## 测试结构

- `conftest.py` - 测试配置和 fixtures（数据库设置、HTTP 客户端）
- `test_users.py` - 用户相关 API 测试
- `test_conversations.py` - 会话相关 API 测试
- `test_messages.py` - 消息相关 API 测试

## 常用命令

```bash
# 运行所有测试
uv run pytest

# 运行指定文件的测试
uv run pytest tests/test_users.py

# 运行指定测试函数
uv run pytest tests/test_users.py::test_create_user

# 显示详细输出
uv run pytest -v

# 显示打印信息
uv run pytest -s

# 失败时停止
uv run pytest -x

# 测试覆盖率
uv run pytest --cov=app
```

## 测试特点

- **完全隔离**：每个测试使用独立的内存数据库，测试后自动清理
- **异步测试**：支持 async/await，测试真实的异步行为
- **依赖注入**：通过覆盖 `get_db` 依赖，无需修改应用代码
