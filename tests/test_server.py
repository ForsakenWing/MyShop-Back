from fastapi.testclient import TestClient
from application.server import app


client = TestClient(app)


class TestServer:

    def test_root(self):
        response = client.get('/')
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
