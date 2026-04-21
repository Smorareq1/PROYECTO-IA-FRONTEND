"""Tests for the /api/v1/auth endpoints."""


class TestLogin:
    def test_login_success(self, client):
        resp = client.post("/api/v1/auth/login", json={
            "email": "admin@demo.com",
            "password": "admin123",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["user"]["email"] == "admin@demo.com"
        assert data["user"]["role"] == "admin"

    def test_login_wrong_password(self, client):
        resp = client.post("/api/v1/auth/login", json={
            "email": "admin@demo.com",
            "password": "wrongpassword",
        })
        assert resp.status_code == 401

    def test_login_nonexistent_user(self, client):
        resp = client.post("/api/v1/auth/login", json={
            "email": "nobody@example.com",
            "password": "test",
        })
        assert resp.status_code == 401

    def test_login_all_demo_users(self, client):
        users = [
            ("admin@demo.com", "admin123", "admin"),
            ("agente@demo.com", "agente123", "agente"),
            ("cliente@demo.com", "cliente123", "cliente"),
        ]
        for email, password, role in users:
            resp = client.post("/api/v1/auth/login", json={
                "email": email, "password": password,
            })
            assert resp.status_code == 200
            assert resp.json()["user"]["role"] == role


class TestMe:
    def test_me_with_valid_token(self, client, auth_header):
        resp = client.get("/api/v1/auth/me", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "admin@demo.com"
        assert "id" in data
        assert "full_name" in data
        assert "role" in data
        assert "created_at" in data

    def test_me_without_token(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_with_invalid_token(self, client):
        resp = client.get("/api/v1/auth/me", headers={
            "Authorization": "Bearer invalid.token.here",
        })
        assert resp.status_code == 401


class TestRefresh:
    def test_refresh_success(self, client):
        # First login to get a refresh token
        login_resp = client.post("/api/v1/auth/login", json={
            "email": "admin@demo.com",
            "password": "admin123",
        })
        refresh_token = login_resp.json()["refresh_token"]

        # Use it to get a new access token
        resp = client.post("/api/v1/auth/refresh", json={
            "refresh_token": refresh_token,
        })
        assert resp.status_code == 200
        assert "access_token" in resp.json()

    def test_refresh_invalid_token(self, client):
        resp = client.post("/api/v1/auth/refresh", json={
            "refresh_token": "invalid.token",
        })
        assert resp.status_code == 401


class TestLogout:
    def test_logout(self, client, auth_header):
        resp = client.post("/api/v1/auth/logout", headers=auth_header)
        assert resp.status_code == 204

    def test_logout_without_auth(self, client):
        resp = client.post("/api/v1/auth/logout")
        assert resp.status_code == 401
