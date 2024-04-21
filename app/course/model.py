from datetime import timedelta
from sqlalchemy import String
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel, Session, select
from conf.database import async_engine

from app.base.model import BaseModelType
from app.user.model import User


class CourseBase(SQLModel):
    title: str = Field(
        index=True,
        nullable=False,
        max_length=200,
        unique=True,
        allow_mutation=True,
        title="Course Title",
        sa_type=String(200),
    )
    description: str = Field(
        nullable=True,
        max_length=1000,
        allow_mutation=True,
        title="Course Description",
    )
    duration: timedelta = Field(
        nullable=True,
    )

    price: float = Field(
        nullable=True,
        gt=0,
        default=0.0,
    )

    @field_validator("duration", mode="before")
    async def duration_minute_validation(cls, timestamp):
        if isinstance(timestamp, int):
            timestamp = timedelta(minutes=timestamp)
        return timestamp


# Properties to receive via API on creation
class CourseCreate(CourseBase):
    instructor_id: int | None = Field(
        default=None, foreign_key="user.id", nullable=False
    )

    @field_validator("instructor_id", mode="before")
    async def user_instructor_validation(cls, instructor_id):
        if isinstance(instructor_id, int):
            async with Session(async_engine) as session:
                statement = select(User).where(
                    User.id == instructor_id, User.is_instructor
                )
                instructor = await session.exec(statement)
                if not instructor:
                    raise ValueError(
                        f"Instructor not found with given id {instructor_id}"
                    )
        return instructor_id


# Database model, database table inferred from class name
class Course(CourseCreate, BaseModelType, table=True):
    instructor: User | None = Relationship(back_populates="courses")
