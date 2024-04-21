from typing import TYPE_CHECKING, List, Self
from datetime import datetime

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession
from conf.database import async_engine

from app.base.model import BaseModelType

if TYPE_CHECKING:
    from app.course.model import Course
    from app.user.model import User


class EnrollBase(SQLModel):
    student_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    course_id: int | None = Field(default=None, foreign_key="course.id", nullable=False)
    enroll_date: datetime = Field(
        default_factory=datetime.now(),
    )


# Properties to receive via API on creation
class EnrollCreate(EnrollBase):
    @field_validator("student_id", mode="after")
    async def user_student_validation(cls, student_id):
        if isinstance(student_id, int):
            async with AsyncSession(async_engine) as session:
                statement = select(User).where(User.id == student_id, User.is_student)
                student = await session.exec(statement)
                if student.one_or_none() is None:
                    raise ValueError(f"Student not found with given id {student_id}")
                return student

    @field_validator("course_id", mode="after")
    async def course_validation(cls, course_id):
        if isinstance(course_id, int):
            async with AsyncSession(async_engine) as session:
                statement = select(Course).where(
                    Course.id == course_id
                )
                course = await session.exec(statement)
                if course.one_or_none() is None:
                    raise ValueError(f"Course not found with given id {course_id}")
                return course

    # @model_validator(mode="after")
    # def verify_enrollment(self) -> Self:
    #     if self.is_instructor and not self.is_student:
    #         return self
    #     elif self.is_student and not self.is_instructor:
    #         return self
    #     raise ValueError("user can only be student or instructor")


# Database model, database table inferred from class name
class Enrollment(EnrollCreate, BaseModelType, table=True):
    course: List["Course"] = Relationship(back_populates="enrolls")
    student: List["User"] = Relationship(back_populates="enrolls")
