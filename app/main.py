"""Talented DevOps mikroservisi - Hafta 5 CI/CD sürümü."""
import os

import psycopg2
from fastapi import FastAPI, Response

APP_VERSION = os.getenv("APP_VERSION", "dev")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "postgres")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")

app = FastAPI(title="Talented DevOps Service", version=APP_VERSION)


def check_database() -> str:
    """PostgreSQL bağlantısını dener; DB tanımlı değilse 'skipped' döner."""
    if not DB_HOST:
        return "skipped"
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            connect_timeout=3,
        )
        conn.close()
        return "connected"
    except psycopg2.OperationalError as exc:
        return f"disconnected: {exc}"


@app.get("/")
def root() -> dict:
    """Servis tanıtım uç noktası."""
    return {"service": "talented-devops", "version": APP_VERSION}


@app.get("/version")
def version() -> dict:
    """Çalışan imajın sürüm bilgisini döner."""
    return {"version": APP_VERSION}


@app.get("/healthz")
def health_check(response: Response) -> dict:
    """Sağlık kontrolü: API ve veritabanı durumu."""
    db_status = check_database()
    healthy = db_status in ("connected", "skipped")
    if not healthy:
        response.status_code = 503
    return {
        "status": "healthy" if healthy else "unhealthy",
        "checks": {"api": "ok", "database": db_status},
    }
