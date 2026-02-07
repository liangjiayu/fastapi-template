from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional


# 1. 基础模型：定义用户模块通用的字段
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="有效的电子邮箱")


# 2. 创建用户模型：用户注册时需要传密码
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="密码，至少6位")


# 3. 输出用户模型：返回给前端的数据格式
class UserOut(UserBase):
    id: int
    created_at: datetime

    # 关键：这行配置允许 Pydantic 兼容 SQLAlchemy 的模型对象
    model_config = ConfigDict(from_attributes=True)
