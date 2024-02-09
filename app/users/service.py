from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate


class UserService:
    """
    Database access object for User model
    Докстринги на методы не писал, тк все и так очевидно
    """
    model = User

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_data: UserCreate):
        db_user = User(username=user_data.username, email=user_data.email)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def get_users(self, page: int, limit: int):
        """
        :param limit: number of users on the page
        """
        offset_min = page * limit
        offset_max = (page + 1) * limit

        users = self.session.query(User).all()[offset_min:offset_max]
        return {"page": page, "limit": limit, "users": users[offset_min:offset_max]}

    def get_user(self, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def update_user(self, user_id: int, user: UserUpdate):
        db_user = self.session.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        if user.username is not None:
            db_user.username = user.username
        if user.email is not None:
            db_user.email = user.email
        self.session.commit()
        self.session.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int):
        db_user = self.session.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        self.session.delete(db_user)
        self.session.commit()
        return {"message": "User deleted successfully"}

    def count_recent_users(self) -> int:
        """
        Count the number of users registered in the last 7 days.
        """
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        recent_users_count = self.session.query(func.count(User.id)).filter(User.registration_date >= week_ago).scalar()
        return recent_users_count

    def top_users_with_longest_names(self) -> list[User]:
        """
        Return the top 5 users with the longest names.
        """
        top_users = self.session.query(User).order_by(func.length(User.username).desc()).limit(5).all()
        return top_users

    def email_domain_percentage(self, domain: str) -> float:
        """
        Calculate the percentage of users with email addresses registered in the specified domain.
        """
        total_users = self.session.query(func.count(User.id)).scalar()
        users_with_domain = self.session.query(func.count(User.id)).filter(User.email.like(f"%@{domain}")).scalar()
        if total_users > 0:
            domain_percentage = (users_with_domain / total_users) * 100
        else:
            domain_percentage = 0.0
        return domain_percentage
