from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.execution_service import get_execution
from app.scheduler.scheduler import get_ready_tasks


router = APIRouter(
    prefix="/scheduler",
    tags=["Scheduler"]
)


@router.get(
    "/executions/{execution_id}/ready-tasks"
)
def get_ready_tasks_for_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    execution = get_execution(
        db,
        execution_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found."
        )

    ready_tasks = get_ready_tasks(
        db,
        execution_id
    )

    return {
        "execution_id": execution_id,
        "ready_tasks": [
            {
                "task_execution_id": task.id,
                "task_id": task.task_id,
                "status": "READY"
            }
            for task in ready_tasks
        ]
    }