from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services.worker_monitor import detect_failed_workers

from app.db.database import get_db
from app.services.worker_service import (
    register_worker,
    update_heartbeat,
    get_workers
)

router = APIRouter(
    prefix="/workers",
    tags=["Workers"]
)


@router.post("/register")
def register_worker_api(
    worker_name: str,
    db: Session = Depends(get_db)
):
    worker = register_worker(db, worker_name)

    return {
        "id": worker.id,
        "worker_name": worker.worker_name,
        "status": worker.status,
        "last_heartbeat": worker.last_heartbeat
    }


@router.post("/{worker_id}/heartbeat")
def heartbeat(
    worker_id: int,
    db: Session = Depends(get_db)
):
    worker = update_heartbeat(db, worker_id)

    if worker is None:
        raise HTTPException(
            status_code=404,
            detail="Worker not found."
        )

    return {
        "worker_id": worker.id,
        "status": worker.status,
        "last_heartbeat": worker.last_heartbeat
    }


@router.get("/")
def list_workers(
    db: Session = Depends(get_db)
):
    workers = get_workers(db)

    return [
        {
            "id": worker.id,
            "worker_name": worker.worker_name,
            "status": worker.status,
            "last_heartbeat": worker.last_heartbeat
        }
        for worker in workers
    ]

@router.post("/monitor")
def monitor_workers(
    db: Session = Depends(get_db)
):
    failed_workers = detect_failed_workers(db)

    return {
        "failed_workers": [
            {
                "id": worker.id,
                "worker_name": worker.worker_name,
                "status": worker.status
            }
            for worker in failed_workers
        ]
    }