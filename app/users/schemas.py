from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserActivity(BaseModel):
    """
    Schema for output user activity data
    """
    next_month_activity: int


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


class UserInfoOut(UserOut):
    """
    Schema for output user data
    """
    id: int
    username: str
    email: str
    registration_date: datetime
    activity_probability_next_month: float | None


class UsersPaginatedOut(BaseModel):
    """
    Schema for output when reading a user list with pagination support
    """
    page: int
    limit: int
    users: list[UserOut]


class UserStatistics(BaseModel):
    """
    Schema for output when reading a user list with pagination support
    """
    recent_users_count: int
    top_users_with_longest_names: list
    email_domain_percentage: float
