def _auth(client, username="user1", password="pw123456"):
    client.post("/api/auth/register", json={"username": username, "password": password})
    r = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_pagination(client):
    h = _auth(client)
    for i in range(25):
        client.post("/api/notes", headers=h, json={"title": f"N{i:02d}", "content": ""})

    r = client.get("/api/notes", headers=h, params={"limit": 10, "offset": 0})
    body = r.json()
    assert body["total"] == 25
    assert body["limit"] == 10
    assert body["offset"] == 0
    assert len(body["items"]) == 10

    r = client.get("/api/notes", headers=h, params={"limit": 10, "offset": 20})
    body = r.json()
    assert body["total"] == 25
    assert len(body["items"]) == 5


def test_pagination_bounds(client):
    h = _auth(client)
    # limit must be in [1, 200]
    assert client.get("/api/notes", headers=h, params={"limit": 0}).status_code == 422
    assert client.get("/api/notes", headers=h, params={"limit": 201}).status_code == 422
    assert client.get("/api/notes", headers=h, params={"offset": -1}).status_code == 422
