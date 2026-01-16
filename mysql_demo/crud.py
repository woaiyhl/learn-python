from typing import List, Optional

# Session 是 SQLAlchemy 的会话对象，用于执行所有数据库操作
from sqlalchemy.orm import Session

# models 中是 ORM 模型定义，schemas 中是 Pydantic 模型
from . import models, schemas


# 根据主键 ID 查询单个学生
def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


# 分页查询学生列表
def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    return db.query(models.Student).offset(skip).limit(limit).all()


# 通过邮箱查询学生，用于检查是否已注册
def get_student_by_email(db: Session, email: str) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.email == email).first()


# 创建学生记录，将 Pydantic 模型转换为 ORM 模型并插入数据库
def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    db_student = models.Student(name=student.name, email=student.email, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


# 更新学生信息（只更新传入的字段）
def update_student(
    db: Session, student_id: int, student: schemas.StudentUpdate
) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if db_student is None:
        return None
    if student.name is not None:
        db_student.name = student.name
    if student.age is not None:
        db_student.age = student.age
    db.commit()
    db.refresh(db_student)
    return db_student


# 删除学生记录，如果不存在则返回 None
def delete_student(db: Session, student_id: int) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if db_student is None:
        return None
    db.delete(db_student)
    db.commit()
    return db_student
