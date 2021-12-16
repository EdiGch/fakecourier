from fastapi.testclient import TestClient

from app.conf import settings


def test_version_get(client: TestClient) -> None:
    r = client.get("/version")
    msg = r.json()
    assert msg == settings.VERSION
