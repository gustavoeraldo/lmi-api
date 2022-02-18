from fastapi.testclient import TestClient

from main import app
from app.v1.core.config import settings

client = TestClient(app)


def test_failure_non_existing_user():
    body = {
        "email": "fake_email@gmail.com",
        "password": "somepassword",
    }

    response = client.post(url="/token", json=body)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "There is no user with the given email address or wrong email"
    }


def test_wrong_password():
    body = {
        "email": settings.TEST_EMAIL_ADMIN,
        "password": "somepassword",
    }

    response = client.post(url="/token", json=body)
    assert response.status_code == 400
    assert response.json() == {"detail": "Wrong password, try again."}

def test_get_successfully_token():
    body = {
        "email": settings.TEST_EMAIL_ADMIN,
        "password": settings.TEST_PASSWORD,
    }

    response = client.post(url="/token", json=body)
    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"]
