from datetime import datetime

from sqlmodel import Field

from app.models import SQLModel


# Shared properties
class TimeStampedModel(SQLModel):
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
