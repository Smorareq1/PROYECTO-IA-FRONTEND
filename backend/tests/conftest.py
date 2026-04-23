"""
Shared pytest fixtures for the TicketAI backend test suite.
"""
import os
import tempfile

import pytest
from fastapi.testclient import TestClient

# Point DATABASE_PATH to a temp file BEFORE importing anything from app
_tmp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
os.environ["DATABASE_PATH"] = _tmp_db.name
_tmp_db.close()


@pytest.fixture(scope="session")
def trained_model():
    """Load the real trained model once for the entire test session."""
    from app.naive_bayes.model_io import load_model
    from app.config import MODEL_PATH
    from pathlib import Path

    model_path = Path(MODEL_PATH)
    if not model_path.exists():
        pytest.skip("Trained model not found — run 'python -m scripts.train' first")
    return load_model(str(model_path))


@pytest.fixture(scope="session")
def client():
    """
    FastAPI TestClient with lifespan (DB init, model load).
    Uses a temporary SQLite database so tests don't pollute production data.
    """
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
def auth_header(client):
    """Get a valid Bearer token for admin@demo.com."""
    resp = client.post("/api/v1/auth/login", json={
        "email": "admin@demo.com",
        "password": "admin123",
    })
    assert resp.status_code == 200, f"Login failed: {resp.text}"
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(scope="session")
def cliente_header(client):
    """Get a valid Bearer token for cliente@demo.com."""
    resp = client.post("/api/v1/auth/login", json={
        "email": "cliente@demo.com",
        "password": "cliente123",
    })
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
