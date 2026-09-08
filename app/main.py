from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.database import engine, init_db
from app.db.redis import check_redis_connection


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)


@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def root():
    return {
        "message": "Distributed Workflow Engine API"
    }


@app.get("/health")
def health_check():

    health_status = {
        "api": "healthy",
        "database": "unknown",
        "redis": "unknown"
    }

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        health_status["database"] = "healthy"

    except Exception:
        health_status["database"] = "unhealthy"

    try:
        check_redis_connection()

        health_status["redis"] = "healthy"

    except Exception:
        health_status["redis"] = "unhealthy"

    return health_status