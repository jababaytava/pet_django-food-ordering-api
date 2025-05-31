from unittest.mock import patch

import pytest
from django.urls import reverse
from orders.models import Order, OrderItem


@pytest.mark.django_db
@patch("orders.serializers.confirm_order_task.delay")
def test_create_order(mock_celery, auth_client, dishes, table):
    url = reverse("order-create")
    payload = {
        "table": table.id,
        "items": [
            {"dish": dishes[0].id, "quantity": 2},
            {"dish": dishes[1].id, "quantity": 1},
        ],
    }

    response = auth_client.post(url, payload, format="json")

    assert response.status_code == 201
    data = response.json()

    assert data["table"] == table.id
    assert len(data["items"]) == 2

    mock_celery.assert_called_once()
    assert Order.objects.count() == 1
    assert OrderItem.objects.count() == 2


@pytest.mark.django_db
def test_create_order_with_inactive_dish(auth_client, inactive_dish, table):
    url = reverse("order-create")
    payload = {"table": table.id, "items": [{"dish": inactive_dish.id, "quantity": 1}]}

    response = auth_client.post(url, payload, format="json")

    assert response.status_code == 400
    assert "items" in response.data
    assert any("not available" in str(err) for err in response.data["items"])


@pytest.mark.django_db
@patch("orders.serializers.confirm_order_task.delay")
def test_get_order_list(mock_celery, auth_client, dishes, table):
    url_create = reverse("order-create")
    payload = {"table": table.id, "items": [{"dish": dishes[0].id, "quantity": 1}]}
    auth_client.post(url_create, payload, format="json")

    url_list = reverse("order-list")
    response = auth_client.get(url_list)

    assert response.status_code == 200
    data = response.json()
    mock_celery.assert_called_once()
    assert len(data) == 1
    assert data[0]["table"] == table.id
