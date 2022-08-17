from requests import request
from src.core import Token, Data, User
from tests.Common.base_v1 import BaseV1
import pytest


@pytest.fixture(scope="module", autouse=True, name="url")
def url_fixture() -> str:
    url = "http://0.0.0.0:8088"
    return url


class TestV1EndToEnd:

    def test_create_new_user(self, url):
        response = request(
            method="post",
            url=f"{url}/api/v1/user/new",
            json=dict(
                username="test_user_to_get_token",
                email="user@example.com",
                password="test_password",
            )
        )
        BaseV1.token = response.json()['data']['token']['access_token']
        assert response.status_code == 201
        assert Data.validate(response.json()['data'])

    def test_login_for_access_token(self, url):
        response = request(
            method="post",
            url=f"{url}/api/v1/user/token",
            data=dict(
                username="test_user_to_get_token",
                password="test_password"
            )
        )
        assert response.status_code == 200
        assert Token.validate(response.json())

    def test_get_user_data(self, url):
        response = request(
            method="get",
            url=f"{url}/api/v1/user/me",
            headers={"Authorization": f'Bearer {BaseV1.token}'}
        )
        assert response.status_code == 200
        assert User.validate(response.json())

    def test_delete_user(self, url):
        response = request(
            method="delete",
            url=f"{url}/api/v1/user/me/delete",
            headers={"Authorization": f'Bearer {BaseV1.token}'}
        )
        assert response.status_code == 200
        assert response.json() == {"Status": "Successful removing"}
