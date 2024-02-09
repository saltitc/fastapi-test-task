from fastapi import APIRouter, Query

from app.database import SessionLocal
from app.users.activity.models import UserActivity
from app.users.activity.service import ActivityPredictionService
from app.users.schemas import (UserCreate, UserInfoOut, UserOut,
                               UsersPaginatedOut, UserStatistics, UserUpdate)
from app.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)
UserService = UserService(SessionLocal())
ActivityPredictionService = ActivityPredictionService()


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


@router.get("/{user_id}", response_model=UserInfoOut)
def get_user(user_id: int):
    """
    API endpoint for obtaining information about a user by his id
    """
    user = UserService.get_user(user_id)
    user_activity = user.activity[0] if user.activity else None
    if user_activity:
        user_activity_data = {
            "visits": user_activity.visits,
            "actions": user_activity.actions,
            "session_duration": user_activity.session_duration
        }
        user_activities = SessionLocal().query(UserActivity).all()
        activity_model = ActivityPredictionService.train_model(user_activities)
        activity_probability = ActivityPredictionService.predict_activity_probability(activity_model,
                                                                                      user_activity_data)
    else:
        activity_probability = None

    user_data_with_activity = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "registration_date": user.registration_date,
        "activity_probability_next_month": activity_probability
    }
    return user_data_with_activity


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


@router.get("/statistics/", response_model=UserStatistics)
def user_statistics(domain: str = Query(default=None)):
    """
    Get user statistics including the number of users registered in the last 7 days,
    top 5 users with the longest names, and the percentage of users with email addresses
    in the specified domain.
    """
    recent_users_count = UserService.count_recent_users()
    top_users = UserService.top_users_with_longest_names()
    domain_percentage = None
    if domain:
        domain_percentage = UserService.email_domain_percentage(domain)
    return {
        "recent_users_count": recent_users_count,
        "top_users_with_longest_names": [user.username for user in top_users],
        "email_domain_percentage": domain_percentage
    }
