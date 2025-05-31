import pytest
from django.urls import reverse
from users.models import User
from unittest.mock import patch


@pytest.mark.django_db
@patch("users.services.user_service.send_welcome_email.delay")
def test_user_registration(mock_send_email, client):
    url = reverse("register")
    payload = {
        "username": "test",
        "email": "newuser@example.com",
        "password": "strongpassword123",
    }

    response = client.post(url, payload, format="json")

    assert response.status_code == 201
    assert User.objects.filter(email="newuser@example.com").exists()
    mock_send_email.assert_called_once()
