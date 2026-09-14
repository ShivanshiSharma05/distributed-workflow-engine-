from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task_execution import TaskExecution
from app.schemas.task_execution import (
    TaskExecutionStatusUpdate,
    TaskExecutionResponse
)
from app.services.execution_service import update_workflow_status

router = APIRouter(
    prefix="/task-executions",
    tags=["Task Executions"]
)

@router.put(
    "/{task_execution_id}/status",
    response_model=TaskExecutionResponse
)
def update_task_execution_status(
    task_execution_id: int,
    status_data: TaskExecutionStatusUpdate,
    db: Session = Depends(get_db)
):

    task_execution = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.id == task_execution_id
        )
        .first()
    )

    if task_execution is None:
        raise HTTPException(
            status_code=404,
            detail="Task execution not found."
        )

    task_execution.status = status_data.status

    db.commit()
    db.refresh(task_execution)

    update_workflow_status(
        db,
        task_execution.workflow_execution_id
    )

    return task_execution