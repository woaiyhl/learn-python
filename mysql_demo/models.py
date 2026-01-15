from sqlalchemy import Column, Integer, String

from .database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, index=True)
    email = Column(String(100), nullable=False, unique=True, index=True)
    age = Column(Integer, nullable=True)

