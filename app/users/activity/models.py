from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


class UserActivity(Base):
    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    visits = Column(Integer)
    actions = Column(Integer)
    session_duration = Column(Float)
    next_month_activity = Column(Integer)  # (1 - active, 0 - inactive)

    user = relationship("User", back_populates="activity")
