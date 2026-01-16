from sqlalchemy import Column, Integer, String

# Base 是在 database.py 中通过 SQLAlchemy 的 declarative_base 创建的基类
from .database import Base


# Student 是数据库中的学生表 ORM 模型，对应表名 "students"
class Student(Base):
    __tablename__ = "students"

    # 主键 ID，自增整型，并建立索引以加快查询
    id = Column(Integer, primary_key=True, index=True)
    # 学生姓名，最长 50 字符，不能为空，并建立索引
    name = Column(String(50), nullable=False, index=True)
    # 学生邮箱，唯一约束 + 索引，用于登录或去重
    email = Column(String(100), nullable=False, unique=True, index=True)
    # 年龄字段，可以为空（nullable=True 表示可选）
    age = Column(Integer, nullable=True)
