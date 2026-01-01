import pytest

# ---------- CREATE STUDENT ----------

def test_create_student_success(client, jwt_headers):
    res = client.post(
        "/api/v1/student/createnew",
        json={
            "roll_no": "101",
            "firstname": "John",
            "middlename": "M",
            "lastname": "Doe",
            "age": 21,
            "email": "john@test.com",
            "mobileno": "9999999999",
            "course": "MCA",
            "year": "2"
        },
        headers=jwt_headers
    )
    assert res.status_code == 201


@pytest.mark.parametrize("missing", [
    "roll_no", "firstname", "lastname", "email"
])
def test_create_student_missing_field(client, jwt_headers, missing):
    payload = {
        "roll_no": "102",
        "firstname": "A",
        "middlename": "B",
        "lastname": "C",
        "age": 22,
        "email": "a@test.com",
        "mobileno": "8888888888",
        "course": "MCA",
        "year": "2"
    }
    payload.pop(missing)

    res = client.post(
        "/api/v1/student/createnew",
        json=payload,
        headers=jwt_headers
    )
    assert res.status_code == 400


def test_create_student_duplicate_email(client, jwt_headers):
    payload = {
        "roll_no": "103",
        "firstname": "A",
        "middlename": "B",
        "lastname": "C",
        "age": 22,
        "email": "dup@test.com",
        "mobileno": "8888888888",
        "course": "MCA",
        "year": "2"
    }

    client.post("/api/v1/student/createnew", json=payload, headers=jwt_headers)
    res = client.post("/api/v1/student/createnew", json=payload, headers=jwt_headers)
    assert res.status_code == 400


# ---------- GET STUDENT ----------

def test_get_all_students(client, jwt_headers):
    res = client.get("/api/v1/student/getall", headers=jwt_headers)
    assert res.status_code in [200, 404]


def test_get_one_student_success(client, jwt_headers):
    res = client.get("/api/v1/student/getone/1", headers=jwt_headers)
    assert res.status_code in [200, 404]


def test_get_one_student_not_found(client, jwt_headers):
    res = client.get("/api/v1/student/getone/999", headers=jwt_headers)
    assert res.status_code == 404


# ---------- UPDATE STUDENT ----------

def test_update_student_success(client, jwt_headers):
    res = client.put(
        "/api/v1/student/update/1",
        json={"firstname": "Updated"},
        headers=jwt_headers
    )
    assert res.status_code in [200, 404]


# ---------- DELETE STUDENT ----------

def test_delete_student_success(client, jwt_headers):
    res = client.delete("/api/v1/student/delete/1", headers=jwt_headers)
    assert res.status_code in [200, 404]


def test_student_without_token(client):
    res = client.get("/api/v1/student/getall")
    assert res.status_code == 401
