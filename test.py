import pytest
import requests


@pytest.fixture
def get_user():
    return {"username": "johndoe", "password": "secret"}


@pytest.mark.parametrize(
    "input",
    [
        {"outlook": "sunny", "temperature": "mild", "humidity": "normal", "wind": "weak"},
        {"outlook": "sunny", "temperature": "hot", "humidity": "normal", "wind": "weak"},
    ],
)
def test_true(input, get_user):
    login_response = requests.post("http://localhost:8000/token", data=get_user)
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post("http://localhost:8000/playability", json=input, headers=headers)
    assert response.json()["playability"]
