from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="MySQL 学习 API",
    description="使用 FastAPI 和 MySQL 的学生管理示例",
    version="1.0.0",
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境建议设置为具体的域名列表
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法 (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # 允许所有请求头
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/students", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate, db: Session = Depends(get_db)
):
    existing = crud.get_student_by_email(db, email=student.email)
    if existing is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_student(db, student)


@app.get("/students", response_model=List[schemas.Student])
def read_students(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    return crud.get_students(db, skip=skip, limit=limit)


@app.get("/students/{student_id}", response_model=schemas.Student)
def read_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.put("/students/{student_id}", response_model=schemas.Student)
def update_student(
    student_id: int, student: schemas.StudentUpdate, db: Session = Depends(get_db)
):
    db_student = crud.update_student(db, student_id=student_id, student=student)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student


@app.delete("/students/{student_id}", response_model=schemas.Student)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = crud.delete_student(db, student_id=student_id)
    if db_student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student

