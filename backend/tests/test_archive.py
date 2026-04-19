def _auth(client, username="user1", password="pw123456"):
    client.post("/api/auth/register", json={"username": username, "password": password})
    r = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


def test_archive_and_unarchive(client):
    h = _auth(client)
    r = client.post("/api/notes", headers=h, json={"title": "A", "content": ""})
    nid = r.json()["id"]

    r = client.post(f"/api/notes/{nid}/archive", headers=h)
    assert r.status_code == 200
    assert r.json()["archived_at"] is not None

    # Default list excludes archived.
    r = client.get("/api/notes", headers=h)
    assert r.json()["total"] == 0

    # ?archived=true lists archived only.
    r = client.get("/api/notes", headers=h, params={"archived": "true"})
    assert r.json()["total"] == 1

    r = client.post(f"/api/notes/{nid}/unarchive", headers=h)
    assert r.status_code == 200
    assert r.json()["archived_at"] is None

    r = client.get("/api/notes", headers=h)
    assert r.json()["total"] == 1


def test_archive_isolation(client):
    h1 = _auth(client, "alice", "pw123456")
    h2 = _auth(client, "eve", "pw123456")
    r = client.post("/api/notes", headers=h1, json={"title": "A", "content": ""})
    nid = r.json()["id"]
    assert client.post(f"/api/notes/{nid}/archive", headers=h2).status_code == 404
