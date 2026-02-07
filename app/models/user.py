from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from core.database import Base


class User(Base):
    # 告诉 SQLAlchemy，这个类对应数据库中名为 "users" 的表
    __tablename__ = "users"

    # 定义字段
    # primary_key: 主键, index: 创建索引提升查询速度, autoincrement: ID自增
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # String(50): 对应 MySQL 的 VARCHAR(50)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)

    # 存储哈希后的密码（永远不要存明文！）
    hashed_password = Column(String(255), nullable=False)

    # server_default 让数据库在插入时自动生成时间戳
    created_at = Column(DateTime(timezone=True), server_default=func.now())
