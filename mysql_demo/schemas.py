from typing import Optional

# Pydantic 用于数据校验和序列化，是 FastAPI 默认推荐的模型库
# 官方文档：https://docs.pydantic.dev/
from pydantic import BaseModel, EmailStr, Field


# 公共的学生基础字段定义，供创建、更新和返回结果复用
class StudentBase(BaseModel):
    # name 字段必填（...），并限制最大长度为 50
    name: str = Field(..., max_length=50)
    # EmailStr 会自动校验邮箱格式（依赖 email-validator 包）
    email: EmailStr
    # 年龄为可选整数，不填时为 None
    age: Optional[int] = None


# 创建学生时使用的模型，当前与 StudentBase 相同
class StudentCreate(StudentBase):
    pass


# 更新学生时使用的模型，所有字段都变为可选
class StudentUpdate(BaseModel):
    # 更新时可以选择只修改名字
    name: Optional[str] = Field(None, max_length=50)
    # 或只修改年龄
    age: Optional[int] = None


# 返回给前端的学生模型，包含数据库生成的主键 id
class Student(StudentBase):
    id: int

    class Config:
        # from_attributes=True 允许通过 ORM 对象直接构建 Pydantic 模型
        from_attributes = True
