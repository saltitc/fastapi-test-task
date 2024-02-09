import pytest
from app.database import Base, SessionLocalTest, test_engine
from app.users.models import User
from app.users.schemas import UserCreate, UserUpdate
from app.users.service import UserService


class TestUserService:
    """
    Class to test user service
    """

    @pytest.fixture(scope="module")
    def db(self):
        """
        Fixture to set up and tear down the database for testing
        """
        Base.metadata.create_all(bind=test_engine)
        yield
        Base.metadata.drop_all(bind=test_engine)

    def test_create_user_service(self, db):
        """
        Test creating a new user via the UserService
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            user_data = UserCreate(username="test_user", email="test@example.com")
            created_user = user_service.create_user(user_data)
            assert created_user.username == user_data.username
            assert created_user.email == user_data.email

    def test_get_users_service(self, db):
        """
        Test fetching a list of users via the UserService
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            page_data = user_service.get_users(0, 10)
            assert len(page_data["users"]) == 1

    def test_get_user_service(self, db):
        """
        Test fetching a single user by ID via the UserService
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            user_id = 1
            user = user_service.get_user(user_id)
            assert user is not None
            assert user.email == "test@example.com"

    def test_update_user_service(self, db):
        """
        Test updating user information via the UserService
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            user_id = 1
            updated_data = UserUpdate(username="updated_user")
            updated_user = user_service.update_user(user_id, updated_data)
            assert updated_user.username == updated_data.username

    def test_delete_user_service(self, db):
        """
        Test deleting a user via the UserService
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            user_id = 1
            user_service.delete_user(user_id)
            deleted_user = session.query(User).filter(User.id == user_id).first()
            assert deleted_user is None

    def test_count_recent_users(self, db):
        """
        Test counting recent users registered in the last 7 days
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            user_data = UserCreate(username="test_user", email="test@example.com")
            user_service.create_user(user_data)

            user_data = UserCreate(username="test_user2", email="test@gmail.com")
            user_service.create_user(user_data)

            recent_users_count = user_service.count_recent_users()
            assert recent_users_count == 2

    def test_top_users_with_longest_names(self, db):
        """
        Test getting top 5 users with the longest names
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            top_users = user_service.top_users_with_longest_names()
            assert len(top_users) == 2

    def test_email_domain_percentage(self, db):
        """
        Test calculating the percentage of users with email addresses registered in the specified domain
        """
        with SessionLocalTest() as session:
            user_service = UserService(session)
            domain = "example.com"
            domain_percentage = user_service.email_domain_percentage(domain)
            assert domain_percentage == 50.0
