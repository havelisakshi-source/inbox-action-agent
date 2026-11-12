import pytest


REGISTER = {
    "email": "alice@example.com",
    "password": "supersecret123",
    "full_name": "Alice",
}


async def _register(client, payload=None):
    return await client.post("/api/auth/register", json=payload or REGISTER)


async def test_register_success(client):
    resp = await _register(client)
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert body["access_token"]
    assert body["refresh_token"]
    assert body["token_type"] == "bearer"
    assert body["expires_in"] > 0


async def test_register_duplicate_email(client):
    await _register(client)
    resp = await _register(client)
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "conflict"


async def test_register_short_password(client):
    resp = await _register(client, {"email": "bob@example.com", "password": "short"})
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "validation_error"


async def test_login_success(client):
    await _register(client)
    resp = await client.post(
        "/api/auth/login",
        json={"email": REGISTER["email"], "password": REGISTER["password"]},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


async def test_login_wrong_password(client):
    await _register(client)
    resp = await client.post(
        "/api/auth/login",
        json={"email": REGISTER["email"], "password": "wrongpassword"},
    )
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "unauthorized"


async def test_me_requires_token(client):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


async def test_me_returns_user(client):
    reg = await _register(client)
    access = reg.json()["access_token"]
    resp = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {access}"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["email"] == REGISTER["email"]
    assert body["is_active"] is True


async def test_refresh_rotation(client):
    reg = await _register(client)
    old_refresh = reg.json()["refresh_token"]
    resp = await client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert resp.status_code == 200
    new_pair = resp.json()
    assert new_pair["refresh_token"] != old_refresh
    # Old one must be dead
    replay = await client.post("/api/auth/refresh", json={"refresh_token": old_refresh})
    assert replay.status_code == 401


async def test_logout_revokes_refresh(client):
    reg = await _register(client)
    refresh = reg.json()["refresh_token"]
    out = await client.post("/api/auth/logout", json={"refresh_token": refresh})
    assert out.status_code == 204
    resp = await client.post("/api/auth/refresh", json={"refresh_token": refresh})
    assert resp.status_code == 401


async def test_health_endpoint(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"