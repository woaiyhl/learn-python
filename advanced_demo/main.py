from typing import List  # List 用于声明“返回值是列表”这类类型标注
from datetime import timedelta  # timedelta 表示时间间隔，这里用于设置 Token 过期时长

# fastapi: Web 框架核心库
# Depends: 依赖注入工具，这是 FastAPI 的核心特性之一
# FastAPI: 应用类
# HTTPException: 用于抛出 HTTP 错误响应
# status: HTTP 状态码常量
from fastapi import Depends, FastAPI, HTTPException, status

# OAuth2PasswordBearer: OAuth2 密码模式的 Bearer Token 实现
# OAuth2PasswordRequestForm: 用于处理 OAuth2 密码模式的表单数据（username, password）
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from sqlalchemy.orm import (
    Session,
)  # SQLAlchemy 的数据库会话类型，用于依赖注入和类型标注
from jose import JWTError, jwt  # JWTError: JWT 异常类型；jwt: JWT 编解码工具

from . import (
    crud,
    models,
    schemas,
    utils,
)  # 引入本项目的 CRUD、数据库模型、数据校验模型、工具模块
from .database import (
    SessionLocal,
    engine,
)  # SessionLocal: 会话工厂；engine: 数据库引擎（连接入口）

# 创建数据库表
# 这行代码会检查数据库中是否存在对应的表，如果不存在则创建
# 在生产环境中，通常使用 Alembic 进行数据库迁移，而不是这种方式
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="高级博客 API Demo",
    description="包含用户认证(JWT)、文章CRUD的完整示例",
    version="2.0.0",
)


# 依赖项：获取数据库会话
# 这种生成器函数写法配合 Depends 使用，可以确保每个请求都有独立的数据库会话
# 并且在请求处理完成后自动关闭会话（finally 块）
def get_db():
    db = SessionLocal()
    try:
        yield db  # yield 将 db 传递给路径操作函数
    finally:
        db.close()  # 请求结束后关闭连接


# OAuth2 方案配置
# tokenUrl="token" 指定了客户端获取 Token 的相对 URL 路径
# 当在 Swagger UI 中点击"Authorize"按钮时，会向这个 URL 发送请求
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 依赖项：获取当前登录用户
# 这个函数会被用作其他需要认证的接口的依赖
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    1. 接收 Token (FastAPI 会自动从请求头 Authorization: Bearer <token> 中提取)
    2. 解码 Token，获取用户信息 (email)
    3. 从数据库查询用户
    4. 如果一切正常，返回用户对象；否则抛出 401 错误
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # 解码 JWT Token
        payload = jwt.decode(token, utils.SECRET_KEY, algorithms=[utils.ALGORITHM])
        email: str = payload.get(
            "sub"
        )  # 从 payload 中获取 subject (通常是用户 ID 或 Email)
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # 检查用户是否存在
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


# --- 认证路由 ---


@app.post(
    "/token", response_model=schemas.Token, summary="登录获取 Token", tags=["认证"]
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    用户登录接口：
    1. 接收 username (这里作为 email) 和 password
       注意：OAuth2PasswordRequestForm 强制字段名为 'username' 和 'password'
    2. 验证用户凭证
    3. 返回 JWT access token
    """
    # 这里的 form_data.username 对应我们的 email 字段
    user = crud.get_user_by_email(db, email=form_data.username)
    # 验证用户是否存在以及密码是否正确
    if not user or not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成 Token
    access_token_expires = timedelta(minutes=utils.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# --- 用户路由 ---


@app.post("/users/", response_model=schemas.User, summary="注册新用户", tags=["用户"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    注册新用户。会检查邮箱是否已被注册。
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get(
    "/users/me", response_model=schemas.User, summary="获取当前用户信息", tags=["用户"]
)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    """
    获取当前登录用户的详细信息。需要 Bearer Token。
    Depends(get_current_user) 会自动处理 Token 验证
    """
    return current_user


# --- 文章路由 ---


@app.post(
    "/users/me/posts/", response_model=schemas.Post, summary="发布文章", tags=["文章"]
)
def create_post_for_user(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    """
    当前登录用户发布新文章。
    """
    return crud.create_user_post(db=db, post=post, user_id=current_user.id)


@app.get(
    "/posts/", response_model=List[schemas.Post], summary="获取所有文章", tags=["文章"]
)
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取文章列表（公开接口，不需要登录）。
    skip: 跳过多少条
    limit: 限制返回条数
    """
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts
