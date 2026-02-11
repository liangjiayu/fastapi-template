# Alembic 数据库迁移

本目录管理数据库 schema 变更。配置已完成，直接使用命令即可。

## 🚀 常用命令

```bash
# 应用所有迁移
uv run alembic upgrade head

# 回滚最近一次迁移
uv run alembic downgrade -1

# 查看当前版本
uv run alembic current

# 查看迁移历史
uv run alembic history --verbose

# 查看 SQL 预览（不实际执行）
uv run alembic upgrade head --sql
```

## 📝 标准操作流程

### 1. 添加/修改字段

```bash
# 1. 修改模型文件（如 app/models/user.py）
# 2. 生成迁移
uv run alembic revision --autogenerate -m "Add avatar to users"

# 3. 检查生成的文件
cat alembic/versions/xxxxx_add_avatar_to_users.py

# 4. 应用迁移
uv run alembic upgrade head
```

**示例：**
```python
# app/models/user.py
class User(Base):
    avatar = Column(String, nullable=True)  # 新增字段
```

### 2. 添加新表

```bash
# 1. 创建模型文件 app/models/product.py
# 2. ⚠️ 在 alembic/env.py 中导入新模型
# 3. 生成迁移
uv run alembic revision --autogenerate -m "Add products table"
```

**⚠️ 必须在 env.py 导入新模型：**
```python
# alembic/env.py
from app.models.product import Product  # 👈 添加这行
```

否则 autogenerate 检测不到新表！

### 3. 修改字段约束

**场景：将字段从可空改为不可空**

```bash
# 1. 修改模型
# username = Column(String, nullable=True)  # 旧
# username = Column(String, nullable=False) # 新

# 2. 生成迁移
uv run alembic revision --autogenerate -m "Make username not nullable"

# 3. 手动编辑生成的文件，添加数据处理逻辑
```

**需要手动调整迁移文件：**
```python
def upgrade() -> None:
    # 先处理现有空数据
    op.execute("UPDATE users SET username = 'unknown' WHERE username IS NULL")
    # 再修改约束
    op.alter_column('users', 'username', nullable=False)
```

### 4. 添加索引

```python
# app/models/user.py
email = Column(String, index=True)  # 添加 index=True

# 生成迁移（autogenerate 会自动检测）
uv run alembic revision --autogenerate -m "Add index on email"
```

### 5. 重命名字段

**⚠️ autogenerate 会识别为删除+新增，需要手动创建迁移：**

```bash
# 手动创建迁移
uv run alembic revision -m "Rename username to user_name"
```

**手动编写迁移文件：**
```python
def upgrade() -> None:
    op.alter_column('users', 'username', new_column_name='user_name')

def downgrade() -> None:
    op.alter_column('users', 'user_name', new_column_name='username')
```

### 6. 数据迁移

**场景：需要修改现有数据**

```bash
uv run alembic revision -m "Populate default avatar"
```

**手动编写数据迁移：**
```python
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # 使用原始 SQL
    op.execute("""
        UPDATE users
        SET avatar = 'https://example.com/default.png'
        WHERE avatar IS NULL
    """)

def downgrade() -> None:
    # 通常数据迁移的回滚是不可逆的
    pass
```

## ❓ 常见问题

### autogenerate 没有检测到表变更？
**原因：模型未在 env.py 中导入**

检查 `alembic/env.py`：
```python
from app.models.user import User
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.your_model import YourModel  # 👈 确保已导入
```

### 迁移执行失败如何回滚？
```bash
# 回滚最近一次
uv run alembic downgrade -1

# 回滚到指定版本
uv run alembic downgrade <revision_id>

# 回滚到初始状态
uv run alembic downgrade base
```

### 多人开发时迁移冲突？
```bash
# 合并两个分支的迁移
uv run alembic merge <rev1> <rev2> -m "Merge migrations"
```

### 如何查看迁移将执行的 SQL？
```bash
# 预览 SQL（不实际执行）
uv run alembic upgrade head --sql

# 保存到文件
uv run alembic upgrade head --sql > migration.sql
```

## 📂 目录结构

```
alembic/
├── README              # 本文件
├── env.py             # 环境配置（已配置异步，新增模型时需在此导入）
├── script.py.mako     # 迁移脚本模板（不用修改）
└── versions/          # 迁移脚本存储（不要删除历史文件）
    └── xxxx_xxx.py    # 自动生成的迁移文件
```

## ✅ 最佳实践

- ✅ 每次修改模型后立即生成迁移
- ✅ 生成后检查迁移文件逻辑
- ✅ 复杂变更手动编写迁移
- ✅ 提交代码时包含迁移文件
- ✅ 生产环境执行前先预览 SQL
- ❌ 不要修改已应用的迁移文件
- ❌ 不要删除 versions/ 中的历史文件
- ❌ 不要在生产环境使用 downgrade（除非紧急回滚）

## 🔗 更多资源

- Alembic 官方文档: https://alembic.sqlalchemy.org/
- SQLAlchemy 官方文档: https://docs.sqlalchemy.org/
