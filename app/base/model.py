from datetime import datetime, timezone
import sqlalchemy as sa
from sqlmodel import SQLModel, Field


class BaseModelType(SQLModel, abstract=True):
    id: int = Field(
        primary_key=True,
        index=True,
        unique=True,
        nullable=False,
        allow_mutation=False,
    )

    created_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
    updated_at: datetime = Field(
        sa_column=sa.Column(sa.DateTime(timezone=True), nullable=False),
        default_factory=lambda: datetime.now(timezone.utc),
    )
