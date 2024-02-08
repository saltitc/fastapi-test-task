from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for input data when creating a user
    """
    username: str
    email: str


class UserUpdate(BaseModel):
    """
    Schema for input data when updating a user
    """
    username: Optional[str] = None
    email: Optional[str] = None


class UserOut(BaseModel):
    """
    Schema for output user data
    """
    id: int
    username: str
    email: str
    registration_date: datetime


class UsersPaginatedOut(BaseModel):
    """
    Schema for output when reading a user list with pagination support
    """
    page: int
    limit: int
    users: list[UserOut]
