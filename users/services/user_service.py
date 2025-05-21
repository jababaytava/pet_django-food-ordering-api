import logging
from users.repositories.user_repository import UserRepository
from users.models import User
from users.tasks import send_welcome_email

logger = logging.getLogger("users")


class UserService:

    @staticmethod
    def register_user(validated_data) -> User:
        user = UserRepository.create_user(**validated_data)
        logger.info(f"New user registered: {user.email}")
        send_welcome_email.delay(user.email)
        return user
