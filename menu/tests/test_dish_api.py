import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_dish_detail_not_found(client):
    url = reverse("dish-detail", args=[999])
    response = client.get(url)

    assert response.status_code == 404
