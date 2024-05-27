from datetime import timedelta
from pydantic import BaseModel, Field, field_validator



class CourseBase(BaseModel):
    title: str = Field(
        max_length=200,
        title="Course Title",
    )
    description: str = Field(
        max_length=1000,
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


