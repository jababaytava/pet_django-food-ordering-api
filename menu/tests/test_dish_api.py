import pytest

from rest_framework.test import APIClient
from django.urls import reverse
from menu.models import Dish

pytestmark = pytest.mark.django_db


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def dish():
    return Dish.objects.create(
        name="Burger", description="Tasty beef burger", price=9.99, is_available=True
    )


def test_public_can_view_dishes_list(client, dish):
    url = reverse("dish-list")
    response = client.get(url)

    assert response.status_code == 200
    assert any(d["name"] == dish.name for d in response.data)


def test_public_can_view_dish_detail(client, dish):
    url = reverse("dish-detail", kwargs={"pk": dish.pk})
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["name"] == dish.name
    assert float(response.data["price"]) == float(dish.price)
