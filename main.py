from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. 创建应用实例
app = FastAPI(
    title="我的第一个 Python Web 应用",
    description="这是一个基于 FastAPI 的高性能 API 服务",
    version="1.0.0"
)

# 2. 定义数据模型 (Pydantic Model)
# Pydantic 负责数据验证，确保输入输出符合预期的类型
class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True

# 模拟数据库
fake_users_db = [
    {"id": 1, "username": "admin", "email": "admin@example.com", "is_active": True},
    {"id": 2, "username": "guest", "email": "guest@example.com", "is_active": False},
]

# 3. 定义路由 (Path Operation)

@app.get("/", summary="根路径")
async def root():
    """
    访问根路径，返回欢迎信息。
    """
    return {"message": "欢迎来到 Python Web 开发的世界！", "framework": "FastAPI"}

@app.get("/users", response_model=List[User], summary="获取所有用户")
async def read_users(skip: int = 0, limit: int = 10):
    """
    获取用户列表，支持分页参数 skip 和 limit。
    """
    return fake_users_db[skip : skip + limit]

@app.get("/users/{user_id}", response_model=User, summary="根据ID获取用户")
async def read_user(user_id: int):
    """
    通过 ID 查找特定用户。
    """
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
    raise HTTPException(status_code=404, detail="用户未找到")

@app.post("/users", response_model=User, summary="创建新用户")
async def create_user(user: User):
    """
    创建一个新用户。
    """
    # 检查 ID 是否已存在
    for existing_user in fake_users_db:
        if existing_user["id"] == user.id:
            raise HTTPException(status_code=400, detail="用户ID已存在")
    
    fake_users_db.append(user.dict())
    return user
