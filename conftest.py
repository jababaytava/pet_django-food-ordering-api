import pytest
from rest_framework.test import APIClient
from users.models import User
from menu.models import Dish
from tables.models import Table
from django.urls import reverse


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email="user@test.com", username="test_user", password="testpass123"
    )


@pytest.fixture
def auth_client(user):
    client = APIClient()
    url = reverse("token_obtain_pair")
    response = client.post(
        url, {"email": user.email, "password": "testpass123"}, format="json"
    )

    assert response.status_code == 200
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def dishes(db):
    return [
        Dish.objects.create(
            name="Pizza", description="food", price=100, is_available=True
        ),
        Dish.objects.create(
            name="Burger", description="food", price=80, is_available=True
        ),
    ]


@pytest.fixture
def inactive_dish(db):
    return Dish.objects.create(
        name="Hidden", description="food", price=50, is_available=False
    )


@pytest.fixture
def table(db):
    return Table.objects.create(number=5)
