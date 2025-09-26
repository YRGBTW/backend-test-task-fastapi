from datetime import datetime
import pytest

URL =  "/api/v1/auth"

from main import app
from httpx import AsyncClient, ASGITransport

async def register_user(client, email="user@test.com", password="secret", admin_key = None):
    return await client.post(URL+"/register", json={
        "email": email,
        "password": password,
        "admin_key": admin_key
    })

async def login_user(client, email="user@test.com", password="secret"):
    return await client.post(URL+"/login", json={
        "email": email,
        "password": password,
    })

# Simple auth test
@pytest.mark.asyncio
async def test_register_and_login_user(client):
    email = f"user{datetime.now().strftime("%d.%H.%M.%S")}@test.com"

    resp = await register_user(client, email=email, password="test")
    assert resp.status_code == 200

    login = await login_user(client, email=email, password="test")
    assert login.status_code == 200

    tokens = login.json()
    assert "access_token" in tokens and "refresh_token" in tokens

