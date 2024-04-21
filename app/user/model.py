from typing import TYPE_CHECKING, List, Self
from pydantic import model_validator
from sqlalchemy import String
from sqlmodel import Field, Relationship, SQLModel

from app.base.model import BaseModelType

if TYPE_CHECKING:
    from app.course.model import Course

class UserBase(SQLModel):
    name: str = Field(
        index=True,
        nullable=False,
        max_length=50,
        unique=True,
        allow_mutation=True,
        title="Course Title",
        sa_type=String(50),
    )
    is_student: bool = Field(default=True)
    is_instructor: bool = Field(default=False)


# Properties to receive via API on creation
class UserCreate(UserBase):
    @model_validator(mode='after')
    def verify_user_type(self) -> Self:
        if self.is_instructor and not self.is_student:
            return self
        elif self.is_student and not self.is_instructor:
            return self
        raise ValueError("user can only be student or instructor")



# Database model, database table inferred from class name
class User(UserBase, BaseModelType, table=True):
    courses: List["Course"] = Relationship(back_populates="students")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
