from datetime import datetime, timedelta
from asyncpg import Record
from pydantic import BaseModel
from fastapi.responses import ORJSONResponse
from fastapi import APIRouter, HTTPException, Request
from fastapi_pagination import LimitOffsetPage, paginate

router = APIRouter(
    prefix="/api/v1",
    tags=["Course"],
    responses={404: {"description": "Not found"}},
)


class CourseBase(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str
    description: str
    duration: timedelta
    price: float
    instructor_id: int


@router.get("/course/{course_id}/")
async def course(request: Request, course_id: int) -> CourseBase:
    if course_id > 0:
        db_conn = request.app.state.get("db_conn")
        course = await db_conn.fetchrow("SELECT * FROM course WHERE id = $1", course_id)
        return dict(course)
    raise HTTPException(status_code=404, detail="Item not found")


@router.get("/courses/", response_class=ORJSONResponse)
async def courses(request: Request) -> LimitOffsetPage[CourseBase]:
    db_conn = request.app.state.get("db_conn")
    courses: Record = await db_conn.fetch("SELECT * FROM course")
    courses = [dict(course) for course in courses]
    return paginate(courses)
