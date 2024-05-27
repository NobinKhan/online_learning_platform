from datetime import datetime
from pydantic import BaseModel, Field, EmailStr



class UserBase(BaseModel):
    full_name: str = Field(
        max_length=100,
        title="User Full Name",
    )
    email: EmailStr = Field(
        max_length=254,
        title="User Email",
    )
    is_student: bool = Field(default=False)
    is_instructor: bool = Field(default=False)


class UserDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
