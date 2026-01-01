import pytest

# ---------- CREATE NEW STAFF ----------

def test_create_staff_success(client, jwt_headers):
    res = client.post(
        "/api/v1/auth/createnew",
        json={
            "name": "User1",
            "email": "user1@test.com",
            "password": "pass123"
        },
        headers=jwt_headers
    )
    assert res.status_code == 201


@pytest.mark.parametrize("payload", [
    {},
    {"name": "A"},
    {"email": "a@test.com"},
    {"password": "123"}
])
def test_create_staff_validation_error(client, jwt_headers, payload):
    res = client.post(
        "/api/v1/auth/createnew",
        json=payload,
        headers=jwt_headers
    )
    assert res.status_code == 400


def test_create_staff_duplicate_email(client, jwt_headers):
    payload = {
        "name": "Dup",
        "email": "dup@test.com",
        "password": "123"
    }
    client.post("/api/v1/auth/createnew", json=payload, headers=jwt_headers)
    res = client.post("/api/v1/auth/createnew", json=payload, headers=jwt_headers)
    assert res.status_code == 400


# ---------- LOGIN ----------

def test_login_success(client):
    res = client.post(
        "/api/v1/auth/login",
        json={"username": "admin@test.com", "password": "admin123"}
    )
    assert res.status_code == 200
    assert "accessToken" in res.json


def test_login_invalid_credentials(client):
    res = client.post(
        "/api/v1/auth/login",
        json={"username": "wrong", "password": "wrong"}
    )
    assert res.status_code == 401


# ---------- LOGOUT ----------

def test_logout_success(client, jwt_headers):
    res = client.post("/api/v1/auth/logout", headers=jwt_headers)
    assert res.status_code == 200


def test_logout_without_token(client):
    res = client.post("/api/v1/auth/logout")
    assert res.status_code == 401


# ---------- REFRESH TOKEN ----------

def test_refresh_token_success(client):
    login = client.post(
        "/api/v1/auth/login",
        json={"username": "admin@test.com", "password": "admin123"}
    )
    refresh = login.json["refreshToken"]

    res = client.post(
        "/api/v1/auth/refreshtoken",
        json={"refreshToken": refresh}
    )
    assert res.status_code == 200
    assert "accessToken" in res.json


def test_refresh_token_invalid(client):
    res = client.post(
        "/api/v1/auth/refreshtoken",
        json={"refreshToken": "invalid"}
    )
    assert res.status_code == 401
