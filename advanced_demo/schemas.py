from typing import (
    List,
    Optional,
)  # List 用于列表类型标注；Optional 表示该字段允许为 None
from pydantic import BaseModel  # Pydantic 的基类，用于数据验证和设置

# Pydantic 模型 (Schemas) 用于定义 API 请求和响应的数据结构
# 它与 SQLAlchemy 模型 (Models) 不同，后者用于定义数据库表结构

# --- Post Schemas (文章相关的模型) ---


class PostBase(BaseModel):
    """文章的基础属性"""

    title: str
    content: Optional[str] = None  # Optional 表示该字段可选，默认为 None


class PostCreate(PostBase):
    """
    创建文章时需要的属性
    继承自 PostBase，所以包含 title 和 content
    通常创建时的模型不需要 id，因为 id 是数据库生成的
    """

    pass


class Post(PostBase):
    """
    用于 API 响应的文章模型（读取文章时返回的数据）
    """

    id: int
    owner_id: int  # 返回文章所属的用户 ID

    class Config:
        # 允许 Pydantic 模型从 ORM 对象（如 SQLAlchemy 模型实例）读取数据
        # 即使数据不是字典而是对象属性（例如 data.id），也能正常工作
        from_attributes = True


# --- User Schemas (用户相关的模型) ---


class UserBase(BaseModel):
    """用户基础属性"""

    email: str


class UserCreate(UserBase):
    """
    创建用户时的属性
    包含密码，因为注册时需要密码
    """

    password: str


class User(UserBase):
    """
    用于 API 响应的用户模型
    注意：这里不包含 password，因为不能把密码（即使是哈希过的）返回给前端
    """

    id: int
    is_active: bool
    posts: List[Post] = []  # 嵌套模型：返回用户发布的所有文章列表

    class Config:
        from_attributes = True


# --- Token Schemas (认证 Token 相关的模型) ---


class Token(BaseModel):
    """登录成功后返回的 Token 信息"""

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Token 解码后的数据结构"""

    email: Optional[str] = None
