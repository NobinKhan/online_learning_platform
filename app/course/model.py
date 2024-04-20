from sqlalchemy import String
from sqlmodel import Field
from app.base.model import BaseModelType

class CourseBase(BaseModelType):
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
    image: str
