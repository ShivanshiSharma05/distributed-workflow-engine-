from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.workflow import Workflow
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
)
from app.services.task_service import (
    create_task,
    get_tasks,
    get_task,
    update_task,
    delete_task,
)


router = APIRouter(
    prefix="/workflows",
    tags=["Tasks"]
)


@router.post(
    "/{workflow_id}/tasks",
    response_model=TaskResponse,
    status_code=201
)
def create_new_task(
    workflow_id: int,
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    workflow = (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return create_task(
        db,
        workflow_id,
        task_data
    )


@router.get(
    "/{workflow_id}/tasks",
    response_model=list[TaskResponse]
)
def list_workflow_tasks(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    workflow = (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return get_tasks(db, workflow_id)


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_single_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return task


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    return update_task(
        db,
        task,
        task_data
    )


@router.delete(
    "/tasks/{task_id}",
    status_code=204
)
def delete_existing_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    delete_task(db, task)

    return None