from users.models import User


class UserRepository:

    @staticmethod
    def create_user(**validated_data) -> User:
        return User.objects.create_user(**validated_data)

    @staticmethod
    def get_by_email(email: str) -> User:
        return User.objects.filter(email=email).first()
