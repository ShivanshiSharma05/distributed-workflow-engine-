from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.database import engine, init_db
from app.db.redis import check_redis_connection

from app.api.workflow import router as workflow_router
from app.api.task import router as task_router
from app.api.dependency import router as dependency_router
from app.api.execution import router as execution_router
from app.api.scheduler import router as scheduler_router
from app.api.task_execution import router as task_execution_router
from app.api.worker import router as worker_router
from app.api.dead_letter import router as dead_letter_router


app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0"
)


app.include_router(workflow_router)
app.include_router(task_router)
app.include_router(dependency_router)
app.include_router(execution_router)
app.include_router(scheduler_router)
app.include_router(task_execution_router)
app.include_router(worker_router)
app.include_router(dead_letter_router)


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