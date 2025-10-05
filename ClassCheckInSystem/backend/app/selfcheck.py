from sqlalchemy import text
from .database import engine, SessionLocal
from .redis_client import redis_client
from .main import app


def check_db():
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


def check_redis():
    redis_client.ping()


def check_app_routes():
    assert any(r.path == "/health" for r in app.routes)


def run():
    check_db()
    check_redis()
    check_app_routes()
    print("Self-check OK: DB, Redis, Routers")


if __name__ == "__main__":
    run()
