from typing import List, Optional

from sqlalchemy.orm import Session

from . import models, schemas


def get_student(db: Session, student_id: int) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_students(db: Session, skip: int = 0, limit: int = 100) -> List[models.Student]:
    return db.query(models.Student).offset(skip).limit(limit).all()


def get_student_by_email(db: Session, email: str) -> Optional[models.Student]:
    return db.query(models.Student).filter(models.Student.email == email).first()


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    db_student = models.Student(name=student.name, email=student.email, age=student.age)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


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


def delete_student(db: Session, student_id: int) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if db_student is None:
        return None
    db.delete(db_student)
    db.commit()
    return db_student

