def _auth(client, username="user1", password="pw123456"):
    client.post("/api/auth/register", json={"username": username, "password": password})
    r = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_bulk_delete(client):
    h = _auth(client)
    ids = []
    for i in range(5):
        r = client.post("/api/notes", headers=h, json={"title": f"N{i}", "content": ""})
        ids.append(r.json()["id"])

    r = client.post("/api/notes/bulk-delete", headers=h, json={"ids": ids[:3]})
    assert r.status_code == 204

    body = client.get("/api/notes", headers=h).json()
    assert body["total"] == 2
    remaining = {n["id"] for n in body["items"]}
    assert remaining == set(ids[3:])


def test_bulk_delete_other_users_notes_ignored(client):
    h1 = _auth(client, "alice", "pw123456")
    h2 = _auth(client, "eve", "pw123456")
    alice_id = client.post("/api/notes", headers=h1, json={"title": "alice", "content": ""}).json()[
        "id"
    ]
    eve_id = client.post("/api/notes", headers=h2, json={"title": "eve", "content": ""}).json()[
        "id"
    ]

    r = client.post("/api/notes/bulk-delete", headers=h2, json={"ids": [alice_id, eve_id]})
    assert r.status_code == 204

    # Alice's note still there.
    assert client.get("/api/notes", headers=h1).json()["total"] == 1
    # Eve's note gone.
    assert client.get("/api/notes", headers=h2).json()["total"] == 0


def test_bulk_delete_validation(client):
    h = _auth(client)
    r = client.post("/api/notes/bulk-delete", headers=h, json={"ids": []})
    assert r.status_code == 422
