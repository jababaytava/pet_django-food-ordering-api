import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from users.models import User
from menu.models import Dish
from orders.models import Order

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", email="user@example.com", password="StrongPass123"
    )


@pytest.fixture
def auth_client(client, user):
    response = client.post(
        reverse("token_obtain_pair"), {"email": user.email, "password": "StrongPass123"}
    )
    token = response.data["access"]
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return client


@pytest.fixture
def dishes():
    return [
        Dish.objects.create(name="Pizza", price=12.99, is_available=True),
        Dish.objects.create(name="Burger", price=9.99, is_available=True),
    ]


def test_create_order(auth_client, dishes):
    for dish in dishes:
        print(dish.id)
    url = reverse("order-create")
    response = auth_client.post(
        url,
        {
            "items": [
                {"dish": dishes[0].id, "quantity": 2},
                {"dish": dishes[1].id, "quantity": 1},
            ]
        },
    )
    assert response.status_code == 201
    assert len(response.data["items"]) == 2


def test_list_orders(auth_client, dishes):
    user = User.objects.get(email="user@example.com")
    order = Order.objects.create(user=user)
    order.items.create(dish=dishes[0], quantity=1)

    url = reverse("order-list")
    response = auth_client.get(url)

    assert response.status_code == 200
    assert len(response.data) >= 1


def test_order_detail(auth_client, dishes):
    user = User.objects.get(email="user@example.com")
    order = Order.objects.create(user=user)
    order.items.create(dish=dishes[0], quantity=1)

    url = reverse("order-detail", kwargs={"pk": order.id})
    response = auth_client.get(url)

    assert response.status_code == 200
    assert response.data["id"] == order.id
