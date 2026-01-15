from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
# Boolean, Integer, String, Text: 定义数据库列的数据类型
# Column: 定义数据库表的列
# ForeignKey: 定义外键，用于关联其他表
from sqlalchemy.orm import relationship  # 用于定义 ORM 层面的关系引用
from .database import Base  # 导入我们在 database.py 中定义的 Base 类

class User(Base):
    """
    用户模型，对应数据库中的 users 表
    继承自 Base，表明这是一个 SQLAlchemy 模型
    """
    __tablename__ = "users"  # 指定数据库中对应的表名

    # 定义各个字段
    # primary_key=True: 设置为主键
    # index=True: 为该列创建索引，加快查询速度
    id = Column(Integer, primary_key=True, index=True)
    # unique=True: 确保邮箱唯一
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)  # 存储哈希后的密码，永远不要存储明文密码
    is_active = Column(Boolean, default=True)  # 用户是否激活状态

    # 建立与 Post 模型的关系
    # relationship 用于在代码层面方便地访问关联数据
    # back_populates="owner" 表示反向引用，Post 模型中也需要有一个 owner 属性指向这里
    posts = relationship("Post", back_populates="owner")


class Post(Base):
    """
    文章模型，对应数据库中的 posts 表
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(Text)  # 使用 Text 类型存储较长的文章内容
    # 定义外键，关联 users 表的 id 字段
    owner_id = Column(Integer, ForeignKey("users.id"))

    # 建立与 User 模型的关系
    # 当访问 post.owner 时，会自动查询对应的 User 对象
    owner = relationship("User", back_populates="posts")
