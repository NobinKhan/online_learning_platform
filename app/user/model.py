from sqlalchemy import String
from sqlmodel import Field, SQLModel

from app.base.model import BaseModelType


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
    pass


# User DB fields
class UserDB(UserBase, BaseModelType):
    is_admin: bool = Field(default=False)


# Database model, database table inferred from class name
class User(UserDB, table=True):
    pass


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int
