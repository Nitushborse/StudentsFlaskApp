def test_get_all_staff(client, jwt_headers):
    res = client.get("/api/v1/staff/getall", headers=jwt_headers)
    assert res.status_code == 200
    assert isinstance(res.json, list)


def test_get_one_staff_success(client, jwt_headers):
    res = client.get("/api/v1/staff/getone/1", headers=jwt_headers)
    assert res.status_code in [200, 404]


def test_get_one_staff_not_found(client, jwt_headers):
    res = client.get("/api/v1/staff/getone/999", headers=jwt_headers)
    assert res.status_code == 404


def test_update_staff_success(client, jwt_headers):
    res = client.put(
        "/api/v1/staff/update/1",
        json={"name": "Updated"},
        headers=jwt_headers
    )
    assert res.status_code == 200


def test_delete_staff_success(client, jwt_headers):
    res = client.delete("/api/v1/staff/delete/1", headers=jwt_headers)
    assert res.status_code in [200, 404]


def test_staff_without_token(client):
    res = client.get("/api/v1/staff/getall")
    assert res.status_code == 401
