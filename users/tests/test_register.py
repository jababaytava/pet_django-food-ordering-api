from django.test import TestCase
from users.serializers import RegisterSerializer
from users.models import User


class RegisterSerializerTest(TestCase):

    def test_valid_data_creates_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "StrongPassword123",
        }

        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertIsInstance(user, User)
        self.assertEqual(user.email, data["email"])
