
import time
import threading
import uuid

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.db.database import SessionLocal

from app.services.queue_service import (
    dequeue_task
)

from app.services.retry_service import (
    retry_task
)

from app.services.worker_service import (
    update_heartbeat
)

from app.models.worker import Worker
from app.models.task import Task
from app.models.task_execution import TaskExecution

from app.models.enums import (
    TaskStatus,
    WorkerStatus
)


def register_worker():
    """
    Register a new worker in PostgreSQL.
    """

    db = SessionLocal()

    try:

        worker_name = (
            f"worker-"
            f"{uuid.uuid4().hex[:8]}"
        )

        worker = Worker(
            worker_name=worker_name,
            status=WorkerStatus.ACTIVE,
            last_heartbeat=(
                datetime.now(timezone.utc)
            )
        )

        db.add(worker)

        db.commit()

        db.refresh(worker)

        print(
            f"Registered worker: "
            f"{worker.worker_name} "
            f"(ID: {worker.id})"
        )

        return worker.id

    finally:

        db.close()


def heartbeat_loop(
    worker_id: int
):
    """
    Send a heartbeat every 5 seconds.
    """

    while True:

        db = SessionLocal()

        try:

            worker = update_heartbeat(
                db,
                worker_id
            )

            if worker:

                print(
                    f"Heartbeat sent by worker "
                    f"{worker.worker_name}"
                )

        except Exception as e:

            print(
                f"Heartbeat error for worker "
                f"{worker_id}: {e}"
            )

        finally:

            db.close()

        time.sleep(5)


def execute_task(
    task_data: dict,
    worker_id: int
):
    """
    Execute one task message.

    Includes basic idempotency protection
    for already-completed task executions.
    """

    db: Session = SessionLocal()

    task_execution_id = (
        task_data["task_execution_id"]
    )

    task_execution = None

    try:

        task_execution = (
            db.query(TaskExecution)
            .filter(
                TaskExecution.id
                == task_execution_id
            )
            .first()
        )

        if task_execution is None:

            print(
                f"Task execution "
                f"{task_execution_id} "
                f"not found."
            )

            return

        # -------------------------------------------------
        # IDEMPOTENCY CHECK
        # -------------------------------------------------

        if task_execution.status in (
            TaskStatus.SUCCESS,
            TaskStatus.DEAD_LETTER
        ):

            print(
                f"Skipping task execution "
                f"{task_execution_id}. "
                f"Current status: "
                f"{task_execution.status}"
            )

            return

        # Only QUEUED tasks should be executed.
        # This prevents accidental execution of
        # PENDING, READY, RUNNING, or RETRYING tasks.
        if task_execution.status != (
            TaskStatus.QUEUED
        ):

            print(
                f"Skipping task execution "
                f"{task_execution_id}. "
                f"Expected QUEUED status, "
                f"but found: "
                f"{task_execution.status}"
            )

            return

        # -------------------------------------------------
        # LOAD TASK DEFINITION
        # -------------------------------------------------

        task = (
            db.query(Task)
            .filter(
                Task.id == task_execution.task_id
            )
            .first()
        )

        if task is None:

            raise Exception(
                f"Task "
                f"{task_execution.task_id} "
                f"not found."
            )

        # -------------------------------------------------
        # MARK TASK AS RUNNING
        # -------------------------------------------------

        task_execution.status = (
            TaskStatus.RUNNING
        )

        task_execution.started_at = (
            datetime.now(timezone.utc)
        )

        task_execution.worker_id = worker_id

        db.commit()

        print(
            f"Starting task execution: "
            f"{task_execution_id}"
        )

        # -------------------------------------------------
        # SIMULATED TASK EXECUTION
        # -------------------------------------------------

        execution_time = 3

        print(
            f"Executing task "
            f"{task_execution.task_id} "
            f"for "
            f"{execution_time} seconds..."
        )

        time.sleep(
            execution_time
        )

        # -------------------------------------------------
        # TIMEOUT CHECK
        # -------------------------------------------------

        if (
            task.timeout_seconds is not None
            and execution_time
            > task.timeout_seconds
        ):

            raise TimeoutError(
                f"Task exceeded timeout of "
                f"{task.timeout_seconds} seconds."
            )

        # -------------------------------------------------
        # MARK TASK AS SUCCESS
        # -------------------------------------------------

        task_execution.status = (
            TaskStatus.SUCCESS
        )

        task_execution.completed_at = (
            datetime.now(timezone.utc)
        )

        db.commit()

        print(
            f"Task execution "
            f"{task_execution_id} "
            f"completed successfully."
        )

    except Exception as e:

        db.rollback()

        task_execution = (
            db.query(TaskExecution)
            .filter(
                TaskExecution.id
                == task_execution_id
            )
            .first()
        )

        if task_execution:

            task_execution.status = (
                TaskStatus.FAILED
            )

            task_execution.error_message = (
                str(e)
            )

            task_execution.completed_at = (
                datetime.now(timezone.utc)
            )

            db.commit()

            print(
                f"Task execution "
                f"{task_execution_id} "
                f"failed: {e}"
            )

            # Retry or move to Dead-Letter Queue.
            retry_task(
                db,
                task_execution
            )

    finally:

        db.close()


def start_worker():
    """
    Register the worker, start heartbeat,
    and continuously consume Redis messages.
    """

    worker_id = register_worker()

    heartbeat_thread = threading.Thread(
        target=heartbeat_loop,
        args=(worker_id,),
        daemon=True
    )

    heartbeat_thread.start()

    print(
        "Worker started."
    )

    print(
        "Waiting for tasks from Redis..."
    )

    while True:

        try:

            task_data = dequeue_task()

            if task_data is None:

                continue

            print(
                f"Received task: "
                f"{task_data}"
            )

            execute_task(
                task_data,
                worker_id
            )

        except KeyboardInterrupt:

            print(
                f"\nWorker "
                f"{worker_id} stopped."
            )

            break

        except Exception as e:

            print(
                f"Worker error: {e}"
            )

            time.sleep(1)


if __name__ == "__main__":

    start_worker()