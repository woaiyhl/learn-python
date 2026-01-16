from typing import List

# FastAPI 是一个现代、快速的 Web API 框架
# 官方文档：https://fastapi.tiangolo.com/
from fastapi import Depends, FastAPI, HTTPException, status

# CORSMiddleware 用于处理跨域资源共享（CORS），让前端能访问后端接口
# CORS 教程：https://fastapi.tiangolo.com/tutorial/cors/
from fastapi.middleware.cors import CORSMiddleware

# Session 是 SQLAlchemy 提供的数据库会话对象，用于执行查询和事务
# SQLAlchemy 官方文档：https://docs.sqlalchemy.org/
from sqlalchemy.orm import Session

# 本项目内部模块：crud 负责数据库读写逻辑，models 定义 ORM 模型，schemas 定义 Pydantic 模型
from . import crud, models, schemas

# SessionLocal 是数据库会话工厂，engine 是数据库连接引擎
from .database import SessionLocal, engine


# 在应用启动时，根据 ORM 模型自动创建数据库表（仅适合学习和 demo 环境）
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MySQL 学习 API",
    description="使用 FastAPI 和 MySQL 的学生管理示例",
    version="1.0.0",
)

# 配置 CORS 中间件，让浏览器前端（例如 React 开发服务器）可以安全调用后端接口
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置为具体的域名列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法 (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # 允许所有请求头
)

# 每个请求获取一个独立的数据库会话，使用 Python 生成器保证用完后自动关闭
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 简单的健康检查接口，用于确认服务是否正常运行
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 创建学生记录，收到前端提交的数据后写入数据库
@app.post("/students", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    # 先根据邮箱检查是否已存在，避免重复注册
    existing = crud.get_student_by_email(db, email=student.email)
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)

# 查询学生列表，支持 skip / limit 分页参数
@app.get("/students", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_students(db, skip=skip, limit=limit)

# 根据学生 ID 查询单条记录
@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# 更新学生信息（目前只允许修改 name 和 age）
@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    db_student = crud.update_student(db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

# 删除学生记录，并返回被删除的那条数据
@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student
