"""Birim testleri - CI boru hattının test aşamasında koşar."""
import psycopg2
from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_root_returns_service_name():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["service"] == "yanlis-isim"


def test_version_endpoint():
    resp = client.get("/version")
    assert resp.status_code == 200
    assert "version" in resp.json()


def test_healthz_without_db_is_healthy(monkeypatch):
    monkeypatch.setattr(main, "DB_HOST", None)
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["checks"]["database"] == "skipped"


def test_healthz_db_connected(monkeypatch):
    class FakeConn:  # pylint: disable=too-few-public-methods
        def close(self):
            return None

    monkeypatch.setattr(main, "DB_HOST", "db")
    monkeypatch.setattr(main.psycopg2, "connect", lambda **kw: FakeConn())
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json()["checks"]["database"] == "connected"


def test_healthz_db_down_returns_503(monkeypatch):
    def boom(**kwargs):
        raise psycopg2.OperationalError("connection refused")

    monkeypatch.setattr(main, "DB_HOST", "db")
    monkeypatch.setattr(main.psycopg2, "connect", boom)
    resp = client.get("/healthz")
    assert resp.status_code == 503
    assert resp.json()["status"] == "unhealthy"
