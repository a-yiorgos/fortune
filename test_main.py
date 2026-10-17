from fastapi.testclient import TestClient
from main import app, fortunes_db

client = TestClient(app)


def test_fortune_help():
    response = client.get("/fortune")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["total_fortunes"] == len(fortunes_db)


def test_fortune_random():
    response = client.get("/fortune/random")
    assert response.status_code == 200
    data = response.json()
    assert "fortune" in data
    assert data["fortune"] in fortunes_db


def test_fortune_nth_valid():
    response = client.get("/fortune/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["fortune"] == fortunes_db[0]

    last_index = len(fortunes_db)
    response_last = client.get(f"/fortune/{last_index}")
    assert response_last.status_code == 200
    data_last = response_last.json()
    assert data_last["id"] == last_index
    assert data_last["fortune"] == fortunes_db[-1]


def test_fortune_nth_out_of_bounds():
    response_zero = client.get("/fortune/0")
    assert response_zero.status_code == 404

    response_negative = client.get("/fortune/-1")
    assert response_negative.status_code == 404

    out_of_range = len(fortunes_db) + 100
    response_high = client.get(f"/fortune/{out_of_range}")
    assert response_high.status_code == 404


def test_fortune_nth_invalid_type():
    response = client.get("/fortune/invalid_string")
    assert response.status_code == 422
