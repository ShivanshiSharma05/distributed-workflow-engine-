from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.worker import Worker
from app.models.enums import WorkerStatus


def register_worker(db: Session, worker_name: str):
    existing_worker = (
        db.query(Worker)
        .filter(Worker.worker_name == worker_name)
        .first()
    )

    if existing_worker:
        existing_worker.status = WorkerStatus.ACTIVE
        existing_worker.last_heartbeat = datetime.now(timezone.utc)

        db.commit()
        db.refresh(existing_worker)

        return existing_worker

    worker = Worker(
        worker_name=worker_name,
        status=WorkerStatus.ACTIVE,
        last_heartbeat=datetime.now(timezone.utc)
    )

    db.add(worker)
    db.commit()
    db.refresh(worker)

    return worker


def update_heartbeat(db: Session, worker_id: int):
    worker = (
        db.query(Worker)
        .filter(Worker.id == worker_id)
        .first()
    )

    if worker is None:
        return None

    worker.last_heartbeat = datetime.now(timezone.utc)
    worker.status = WorkerStatus.ACTIVE

    db.commit()
    db.refresh(worker)

    return worker


def get_workers(db: Session):
    return db.query(Worker).all()