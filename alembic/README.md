# Alembic 数据库迁移

## 常用命令

```bash
uv run alembic upgrade head                          # 应用所有迁移
uv run alembic downgrade -1                          # 回滚最近一次
uv run alembic revision --autogenerate -m "描述"      # 生成迁移（修改模型后）
uv run alembic current                               # 查看当前版本
uv run alembic upgrade head --sql                    # 预览 SQL（不执行）
```

## 添加新模型时

必须在 `alembic/env.py` 中导入新模型，否则 autogenerate 无法检测到：

```python
# alembic/env.py
from app.models.your_model import YourModel  # 添加这行
```
