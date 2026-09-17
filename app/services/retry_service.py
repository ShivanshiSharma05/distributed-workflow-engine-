import time

from sqlalchemy.orm import Session

from app.models.enums import TaskStatus
from app.models.task_execution import TaskExecution
from app.models.task import Task
from app.services.queue_service import enqueue_task


def calculate_backoff(retry_count: int) -> int:
    return 2 ** retry_count


def retry_task(
    db: Session,
    task_execution: TaskExecution
):
    task = (
        db.query(Task)
        .filter(Task.id == task_execution.task_id)
        .first()
    )

    if task is None:
        task_execution.status = TaskStatus.FAILED
        task_execution.error_message = "Task definition not found."
        db.commit()
        return

    if task_execution.retry_count >= task.max_retries:
        task_execution.status = TaskStatus.DEAD_LETTER
        db.commit()

        print(
            f"Task execution {task_execution.id} "
            f"moved to DEAD_LETTER."
        )

        return

    task_execution.retry_count += 1
    task_execution.status = TaskStatus.RETRYING

    db.commit()

    delay = calculate_backoff(task_execution.retry_count)

    print(
        f"Retrying task execution {task_execution.id} "
        f"in {delay} seconds..."
    )

    time.sleep(delay)

    task_data = {
        "task_execution_id": task_execution.id,
        "task_id": task_execution.task_id,
        "workflow_execution_id": task_execution.workflow_execution_id
    }

    enqueue_task(task_data)

    task_execution.status = TaskStatus.QUEUED

    db.commit()

    print(
        f"Task execution {task_execution.id} "
        f"requeued."
    )