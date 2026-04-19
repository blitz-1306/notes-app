def test_register_and_login(client):
    r = client.post("/api/auth/register", json={"username": "alice", "password": "secret123"})
    assert r.status_code == 201
    assert r.json()["username"] == "alice"

    r = client.post(
        "/api/auth/login",
        data={"username": "alice", "password": "secret123"},
    )
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_register_duplicate(client):
    client.post("/api/auth/register", json={"username": "bob", "password": "secret123"})
    r = client.post("/api/auth/register", json={"username": "bob", "password": "otherpass"})
    assert r.status_code == 409


def test_login_bad_password(client):
    client.post("/api/auth/register", json={"username": "carol", "password": "secret123"})
    r = client.post(
        "/api/auth/login",
        data={"username": "carol", "password": "wrong"},
    )
    assert r.status_code == 401


def test_protected_route_requires_token(client):
    r = client.get("/api/notes")
    assert r.status_code == 401
