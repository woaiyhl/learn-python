from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr
    age: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = None


class Student(StudentBase):
    id: int

    class Config:
        from_attributes = True

