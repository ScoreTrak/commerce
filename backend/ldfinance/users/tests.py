from django.urls import reverse
import pytest
from rest_framework import status


class TestCurrentUserView:

    def test_anonymous(self, client):
        response = client.get(reverse("users:current"))
        assert status.is_client_error(response.status_code)
        assert response.json() == {
            "detail": "Authentication credentials were not provided.",
        }

    @pytest.mark.parametrize("is_staff", [True, False])
    def test_authenticated(self, client, django_user_model, is_staff):
        user = django_user_model.objects.create_user("user", is_staff=is_staff)
        client.force_login(user)
        response = client.get(reverse("users:current"))
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"username": "user", "is_staff": is_staff}


@pytest.mark.parametrize("test_username, test_password, expected_status_code", [
    ("admin", "password", status.HTTP_302_FOUND),
    ("admin", "incorrect", status.HTTP_400_BAD_REQUEST),
    ("incorrect", "password", status.HTTP_400_BAD_REQUEST),
])
def test_log_in(client, admin_user, test_username, test_password, expected_status_code):
    response = client.post(reverse("users:log-in"), {
        "username": test_username,
        "password": test_password,
    })
    assert response.status_code == expected_status_code


def test_log_out(admin_client):
    response = admin_client.get(reverse("users:log-out"))
    assert response.status_code == status.HTTP_302_FOUND
