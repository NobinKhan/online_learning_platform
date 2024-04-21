from typing import Any

from pydantic import ValidationError
from starlette.requests import Request

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqladmin import ModelView

from conf.database import async_engine
from app.user.model import User, UserCreate
from app.course.model import Course


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name, User.is_instructor, User.is_student]

    async def insert_model(self, request: Request, data: dict) -> Any:
        data["is_admin"] = False
        try:
            UserCreate(**data)
        except ValidationError as error:
            raise ValueError(error.errors()[0].get("msg"))
        return await super().insert_model(request, data)


class CourseAdmin(ModelView, model=Course):
    column_list = [Course.id, Course.title, Course.instructor]

    async def insert_model(self, request: Request, data: dict) -> Any:
        async with AsyncSession(async_engine) as session:
            statement = select(User).where(
                User.id == int(data.get("instructor")), User.is_instructor
            )
            instructor = await session.exec(statement)
            if instructor.one_or_none() is None:
                raise ValueError(
                    f"Instructor not found or user is not an instructor with id {data.get('instructor')}"
                )
        return await super().insert_model(request, data)
