from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.models.worker import Worker
from app.models.enums import WorkerStatus


HEARTBEAT_TIMEOUT = 15


def detect_failed_workers(db: Session):

    now = datetime.now(timezone.utc)
    threshold = now - timedelta(seconds=HEARTBEAT_TIMEOUT)

    workers = (
        db.query(Worker)
        .filter(
            Worker.status == WorkerStatus.ACTIVE
        )
        .all()
    )

    failed_workers = []

    for worker in workers:

        heartbeat = worker.last_heartbeat

        # Make naive database timestamps timezone-aware
        if heartbeat.tzinfo is None:
            heartbeat = heartbeat.replace(tzinfo=timezone.utc)

        if heartbeat < threshold:
            worker.status = WorkerStatus.UNHEALTHY
            failed_workers.append(worker)

    db.commit()

    return failed_workers