from sqlalchemy.orm import Session

from app.models.enums import TaskStatus
from app.models.task_execution import TaskExecution
from app.services.queue_service import enqueue_task


def dispatch_task(
    db: Session,
    task_execution: TaskExecution
):
    task_data = {
        "task_execution_id": task_execution.id,
        "task_id": task_execution.task_id,
        "workflow_execution_id": task_execution.workflow_execution_id
    }

    enqueue_task(task_data)

    task_execution.status = TaskStatus.QUEUED

    db.commit()
    db.refresh(task_execution)

    return task_execution