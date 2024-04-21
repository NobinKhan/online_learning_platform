from typing import TYPE_CHECKING, List, Self
from datetime import datetime

from pydantic import model_validator
from sqlalchemy import String
from sqlmodel import Field, Relationship, SQLModel

from app.base.model import BaseModelType

if TYPE_CHECKING:
    from app.course.model import Course
    from app.user.model import User



class EnrollBase(SQLModel):
    student_id: int | None = Field(
        default=None, foreign_key="user.id", nullable=False
    )
    course_id: int | None = Field(
        default=None, foreign_key="course.id", nullable=False
    )
    enroll_date: datetime = Field(
        default_factory=datetime.now(),
    )


# Properties to receive via API on creation
class EnrollCreate(EnrollBase):
    @model_validator(mode='after')
    def verify_user_type(self) -> Self:
        if self.is_instructor and not self.is_student:
            return self
        elif self.is_student and not self.is_instructor:
            return self
        raise ValueError("user can only be student or instructor")


# # Database model, database table inferred from class name
# class User(UserDB, table=True):
#     courses: List["Course"] = Relationship(back_populates="instructor")

