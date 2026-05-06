def _register_login(client, username="user1", password="pw123456"):
    client.post("/api/auth/register", json={"username": username, "password": password})
    r = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_change_password(client):
    h = _register_login(client)

    # Wrong old password.
    r = client.post(
        "/api/account/change-password",
        headers=h,
        json={"current_password": "wrong", "new_password": "newpass123"},
    )
    assert r.status_code == 401

    # Correct old password.
    r = client.post(
        "/api/account/change-password",
        headers=h,
        json={"current_password": "pw123456", "new_password": "newpass123"},
    )
    assert r.status_code == 200

    # Old password no longer works.
    r = client.post("/api/auth/login", data={"username": "user1", "password": "pw123456"})
    assert r.status_code == 401

    # New password works.
    r = client.post("/api/auth/login", data={"username": "user1", "password": "newpass123"})
    assert r.status_code == 200


def test_change_password_wrong_current_password_is_rate_limited(client):
    h = _register_login(client)

    for _ in range(5):
        r = client.post(
            "/api/account/change-password",
            headers=h,
            json={"current_password": "wrong", "new_password": "newpass123"},
        )
        assert r.status_code == 401

    r = client.post(
        "/api/account/change-password",
        headers=h,
        json={"current_password": "wrong", "new_password": "newpass123"},
    )
    assert r.status_code == 429


def test_delete_account(client):
    h = _register_login(client, "alice", "pw123456")
    client.post("/api/notes", headers=h, json={"title": "mine", "content": ""})

    # Wrong password.
    r = client.request(
        "DELETE",
        "/api/account",
        headers=h,
        json={"password": "wrong"},
    )
    assert r.status_code == 401

    # Correct password.
    r = client.request(
        "DELETE",
        "/api/account",
        headers=h,
        json={"password": "pw123456"},
    )
    assert r.status_code == 204

    # Subsequent requests with the old token should fail (user gone).
    r = client.get("/api/notes", headers=h)
    assert r.status_code == 401

    # Username can now be taken by a new registration.
    r = client.post("/api/auth/register", json={"username": "alice", "password": "newpass123"})
    assert r.status_code == 201
