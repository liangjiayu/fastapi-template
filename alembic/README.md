# Alembic 数据库迁移

项目使用 Alembic 管理数据库 schema 变更，支持异步引擎（asyncpg / aiosqlite）。

## 目录结构

```
alembic/
├── env.py               # 迁移运行环境（异步引擎配置、模型导入）
├── script.py.mako       # 迁移脚本模板
├── versions/            # 迁移脚本目录（按日期命名）
└── README.md
```

## 常用命令

```bash
uv run alembic upgrade head                          # 应用所有迁移
uv run alembic downgrade -1                          # 回滚最近一次
uv run alembic revision --autogenerate -m "描述"      # 生成迁移（修改模型后）
uv run alembic current                               # 查看当前版本
uv run alembic history                               # 查看迁移历史
uv run alembic upgrade head --sql                    # 预览 SQL（不执行）
```

## 工作流程

### 修改现有模型

```bash
# 1. 修改模型文件（如 app/models/user.py 添加 avatar 字段）
# 2. 生成迁移脚本
uv run alembic revision --autogenerate -m "Add avatar field to users"

# 3. 检查生成的迁移文件，确认 upgrade/downgrade 逻辑正确
# 4. 应用迁移
uv run alembic upgrade head
```

### 添加新模型

新增模型时，**必须**在 `env.py` 中导入，否则 autogenerate 无法检测到：

```python
# alembic/env.py
# 导入所有模型(autogenerate 需要)
from app.models.your_new_model import YourNewModel  # 添加这行
```

然后正常生成迁移即可：

```bash
uv run alembic revision --autogenerate -m "Add your_new_model table"
uv run alembic upgrade head
```

### 回滚迁移

```bash
# 回滚最近一次
uv run alembic downgrade -1

# 回滚到指定版本
uv run alembic downgrade <revision_id>

# 回滚所有（清空数据库）
uv run alembic downgrade base
```

## 配置说明

### 数据库 URL

数据库连接地址从 `app/core/config.py` 的 `settings.DATABASE_URL` 读取，在 `env.py` 中动态设置，无需手动修改 `alembic.ini`。

### 迁移文件命名

迁移文件按日期 + 版本号命名（配置在 `alembic.ini`）：

```
# 格式: 年_月_日_时分-版本号_描述
2026_02_11_2135-5fb242aa5433_initial_schema_with_users_conversations_.py
```

## 注意事项

- **检查生成的迁移**：autogenerate 不是万能的，生成后务必检查 `upgrade()` 和 `downgrade()` 逻辑是否正确
- **不要手动修改 versions 目录中已应用的迁移文件**，会导致版本链断裂
- **Docker 部署**：容器启动时会自动运行 `alembic upgrade head`，无需手动操作
- **团队协作**：多人同时生成迁移可能导致分支冲突，拉取最新代码后再生成迁移
