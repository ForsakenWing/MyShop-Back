from requests import request
from src.core import Token
import pytest


@pytest.fixture(scope="module", autouse=True, name="url")
def url_fixture() -> str:
    url = "http://0.0.0.0:8088"
    return url


class TestV1EndToEnd:

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

    # def test_create_new_user(self):