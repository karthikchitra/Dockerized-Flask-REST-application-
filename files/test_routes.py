import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Health check ──────────────────────────────────────────────────────────────

def test_health_check(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


# ── GET /items ─────────────────────────────────────────────────────────────────

def test_get_items_empty(client):
    res = client.get("/items")
    assert res.status_code == 200
    assert res.get_json()["items"] == []


# ── POST /items ────────────────────────────────────────────────────────────────

def test_create_item(client):
    res = client.post(
        "/items",
        json={"name": "Widget", "description": "A cool widget"},
    )
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Widget"
    assert data["id"] == 1


def test_create_item_missing_name(client):
    res = client.post("/items", json={"description": "No name"})
    assert res.status_code == 400
    assert "error" in res.get_json()


# ── GET /items/<id> ────────────────────────────────────────────────────────────

def test_get_single_item(client):
    client.post("/items", json={"name": "Gadget"})
    res = client.get("/items/1")
    assert res.status_code == 200
    assert res.get_json()["name"] == "Gadget"


def test_get_nonexistent_item(client):
    res = client.get("/items/999")
    assert res.status_code == 404


# ── PUT /items/<id> ────────────────────────────────────────────────────────────

def test_update_item(client):
    client.post("/items", json={"name": "Old Name"})
    res = client.put("/items/1", json={"name": "New Name"})
    assert res.status_code == 200
    assert res.get_json()["name"] == "New Name"


def test_update_nonexistent_item(client):
    res = client.put("/items/999", json={"name": "Ghost"})
    assert res.status_code == 404


# ── DELETE /items/<id> ─────────────────────────────────────────────────────────

def test_delete_item(client):
    client.post("/items", json={"name": "ToDelete"})
    res = client.delete("/items/1")
    assert res.status_code == 200

    res2 = client.get("/items/1")
    assert res2.status_code == 404


def test_delete_nonexistent_item(client):
    res = client.delete("/items/999")
    assert res.status_code == 404
