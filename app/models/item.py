from sqlmodel import Field
from sqlmodel import Relationship

from .base import TimeStampedModel
from .user import User
from app.models import SQLModel


# Shared properties
class ItemBase(SQLModel):
    """ """
    title: str = Field(index=True)
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    """ """
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    """ """
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, TimeStampedModel, table=True):
    """ """
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase, TimeStampedModel):
    """ """
    id: int
    owner_id: int
