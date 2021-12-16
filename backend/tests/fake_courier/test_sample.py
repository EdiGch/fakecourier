import uuid
from fastapi.testclient import TestClient


def test_post_samples_and_get(db, client: TestClient) -> None:
    samples_name_1 = "My samples 1"
    samples_name_2 = "My samples 2"

    request_data_1 = {"name": samples_name_1}
    request_data_2 = {"name": samples_name_2}

    r = client.post(f"/v1/samples", json=request_data_1)
    assert 200 <= r.status_code < 300

    r = client.post(f"/v1/samples", json=request_data_2)
    assert 200 <= r.status_code < 300

    r = client.get(f"/v1/samples")
    assert 200 <= r.status_code < 300

    response = r.json()

    assert len(response) == 2


def test_delete_samples(db, client: TestClient) -> None:
    samples_name_1 = "My samples 1"
    request_data_1 = {"name": samples_name_1}

    r = client.post(f"/v1/samples", json=request_data_1)
    assert 200 <= r.status_code < 300

    r = client.get(f"/v1/samples")
    assert 200 <= r.status_code < 300
    data = r.json()
    assert len(data) == 1

    r = client.delete(f"/v1/samples/{data[0]['id']}")
    assert 200 <= r.status_code < 300

    r = client.get(f"/v1/samples")
    assert 200 <= r.status_code < 300
    data = r.json()
    assert len(data) == 0


def test_put_samples(db, client: TestClient) -> None:
    samples_name_1 = "My samples 1"
    samples_name_1_update = "My samples 1 update"

    request_data_1 = {"name": samples_name_1}

    r = client.post(f"/v1/samples", json=request_data_1)
    assert 200 <= r.status_code < 300

    r = client.get(f"/v1/samples")

    assert 200 <= r.status_code < 300
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == samples_name_1

    update_data = {"name": samples_name_1_update}
    r = client.put(f"/v1/samples/{data[0]['id']}", json=update_data)
    assert 200 <= r.status_code < 300

    r = client.get(f"/v1/samples")

    assert 200 <= r.status_code < 300
    data = r.json()
    assert len(data) == 1
    assert data[0]["name"] == samples_name_1_update


def test_not_found(db, client: TestClient) -> None:
    samples_id = str(uuid.uuid4())

    r = client.get(f"/v1/samples/{samples_id}")
    assert r.status_code == 404
