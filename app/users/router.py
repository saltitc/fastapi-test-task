from fastapi import APIRouter, Query

from app.database import SessionLocal
from app.users.schemas import UserCreate, UserOut, UsersPaginatedOut, UserUpdate
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
UserService = UserService(SessionLocal())


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate):
    """
    API endpoint for creating a new user
    """
    return UserService.create_user(user)


@router.get("/", response_model=UsersPaginatedOut)
def get_users(page: int = Query(ge=0, default=0), limit: int = Query(ge=1, le=100, default=10)):
    """
    API endpoint for getting a list of users with pagination support
    :param page: (0 <= number) of page
    :param limit: (1 < number < 100) of users on the page
    """
    return UserService.get_users(page, limit)


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    """
    API endpoint for obtaining information about a user by his id
    """
    return UserService.get_user(user_id)


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserUpdate):
    """
    API endpoint for updating user information
    """
    return UserService.update_user(user_id, user)


@router.delete("/{user_id}")
def delete_user(user_id: int):
    """
    API endpoint for deleting a user
    """
    return UserService.delete_user(user_id)
