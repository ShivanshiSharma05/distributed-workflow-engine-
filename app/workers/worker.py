import time

from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.services.queue_service import dequeue_task
from app.models.task_execution import TaskExecution
from app.models.enums import TaskStatus


def execute_task(task_data: dict):
    db: Session = SessionLocal()

    task_execution_id = task_data["task_execution_id"]

    try:
        task_execution = (
            db.query(TaskExecution)
            .filter(TaskExecution.id == task_execution_id)
            .first()
        )

        if task_execution is None:
            print(f"Task execution {task_execution_id} not found.")
            return

        print(
            f"Starting task execution: "
            f"{task_execution_id}"
        )

        task_execution.status = TaskStatus.RUNNING
        db.commit()

        # Simulate task execution
        print(f"Executing task {task_execution.task_id}...")
        time.sleep(3)

        task_execution.status = TaskStatus.SUCCESS
        db.commit()

        print(
            f"Task execution {task_execution_id} "
            f"completed successfully."
        )

    except Exception as e:
        db.rollback()

        task_execution = (
            db.query(TaskExecution)
            .filter(TaskExecution.id == task_execution_id)
            .first()
        )

        if task_execution:
            task_execution.status = TaskStatus.FAILED
            task_execution.error_message = str(e)
            db.commit()

        print(
            f"Task execution {task_execution_id} failed: {e}"
        )

    finally:
        db.close()


def start_worker():
    print("Worker started.")
    print("Waiting for tasks from Redis...")

    while True:
        task_data = dequeue_task()

        if task_data is None:
            continue

        print(f"Received task: {task_data}")

        execute_task(task_data)


if __name__ == "__main__":
    start_worker()