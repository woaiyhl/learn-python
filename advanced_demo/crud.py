# 引入 SQLAlchemy ORM 的 Session 类型，用于类型注解，表示数据库会话对象
from sqlalchemy.orm import Session
from . import (
    models,
    schemas,
    utils,
)  # 引入本项目的数据库模型、Pydantic 模型、认证/加密工具


def get_user(db: Session, user_id: int):
    """
    根据 ID 获取用户
    db.query(models.User): 创建一个查询对象，目标是 User 模型
    .filter(models.User.id == user_id): 添加过滤条件，相当于 SQL 的 WHERE id = user_id
    .first(): 执行查询并返回第一条结果，如果没有结果则返回 None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """根据邮箱获取用户"""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    """创建新用户"""
    # 1. 对密码进行哈希处理 (安全最佳实践：永远不存储明文密码)
    hashed_password = utils.get_password_hash(user.password)

    # 2. 创建数据库模型实例
    # 注意：这里使用的是 models.User (数据库模型)，而不是 schemas.User (Pydantic 模型)
    db_user = models.User(email=user.email, hashed_password=hashed_password)

    # 3. 添加到会话 (相当于 git add)
    db.add(db_user)

    # 4. 提交事务 (相当于 git commit)，此时数据才真正写入数据库
    db.commit()

    # 5. 刷新实例以获取生成的 ID 和默认值 (因为数据库可能会自动生成 id 等字段)
    db.refresh(db_user)

    return db_user


def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """
    获取文章列表
    .offset(skip): 跳过前 skip 条记录 (用于分页)
    .limit(limit): 最多返回 limit 条记录 (用于分页)
    .all(): 返回所有查询结果的列表
    """
    return db.query(models.Post).offset(skip).limit(limit).all()


def create_user_post(db: Session, post: schemas.PostCreate, user_id: int):
    """创建用户的文章"""
    # **post.dict(): 将 Pydantic 模型转换为字典并解包
    # 相当于 models.Post(title=post.title, content=post.content, owner_id=user_id)
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post
