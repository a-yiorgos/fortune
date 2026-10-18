from fastapi.testclient import TestClient
from main import app, fortunes_db, dict_db, dict_letter_limits

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


# Devil's Dictionary Endpoint Tests


def test_dict_help():
    response = client.get("/dict")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "endpoints" in data
    assert data["total_quotes"] == len(dict_db)
    assert len(dict_db) == 995


def test_dict_lemmata():
    response = client.get("/dict/lemmata")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(dict_db)
    assert data[0] == {"id": 1, "lemma": "ABASEMENT"}
    assert data[-1] == {"id": 995, "lemma": "ZOOLOGY"}

    # Also test alias /dict/lemmas
    response_alias = client.get("/dict/lemmas")
    assert response_alias.status_code == 200
    assert response_alias.json() == data


def test_dict_random():
    response = client.get("/dict/random")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "lemma" in data
    assert "definition" in data
    assert 1 <= data["id"] <= len(dict_db)


def test_dict_nth_valid():
    response_first = client.get("/dict/1")
    assert response_first.status_code == 200
    data_first = response_first.json()
    assert data_first["id"] == 1
    assert data_first["lemma"] == "ABASEMENT"
    assert "ABASEMENT, n." in data_first["definition"]

    response_last = client.get(f"/dict/{len(dict_db)}")
    assert response_last.status_code == 200
    data_last = response_last.json()
    assert data_last["id"] == len(dict_db)
    assert data_last["lemma"] == "ZOOLOGY"
    assert "ZOOLOGY, n." in data_last["definition"]


def test_dict_nth_out_of_bounds():
    response_zero = client.get("/dict/0")
    assert response_zero.status_code == 404

    response_high = client.get(f"/dict/{len(dict_db) + 1}")
    assert response_high.status_code == 404


def test_dict_letter_limits():
    # Test letter 'a' / 'A'
    response_a_lower = client.get("/dict/a")
    assert response_a_lower.status_code == 200
    data_a = response_a_lower.json()
    assert data_a["letter"] == "a"
    assert data_a["min_id"] == 1
    assert data_a["max_id"] == 83

    response_a_upper = client.get("/dict/A")
    assert response_a_upper.status_code == 200
    data_a_upper = response_a_upper.json()
    assert data_a_upper["letter"] == "a"
    assert data_a_upper["min_id"] == 1
    assert data_a_upper["max_id"] == 83

    # Test letter 'b'
    response_b = client.get("/dict/b")
    assert response_b.status_code == 200
    data_b = response_b.json()
    assert data_b["letter"] == "b"
    assert data_b["min_id"] == 84
    assert data_b["max_id"] == 123

    # Test letter 'z'
    response_z = client.get("/dict/z")
    assert response_z.status_code == 200
    data_z = response_z.json()
    assert data_z["letter"] == "z"
    assert data_z["min_id"] == 989
    assert data_z["max_id"] == 995


def test_dict_random_by_letter():
    response_a = client.get("/dict/random/a")
    assert response_a.status_code == 200
    data_a = response_a.json()
    assert "id" in data_a
    assert "lemma" in data_a
    assert "definition" in data_a
    assert 1 <= data_a["id"] <= 83

    response_z = client.get("/dict/random/Z")
    assert response_z.status_code == 200
    data_z = response_z.json()
    assert 989 <= data_z["id"] <= 995


def test_dict_invalid_param():
    response_invalid_str = client.get("/dict/invalid_multi_char")
    assert response_invalid_str.status_code == 404

    response_invalid_letter_rand = client.get("/dict/random/123")
    assert response_invalid_letter_rand.status_code == 404
