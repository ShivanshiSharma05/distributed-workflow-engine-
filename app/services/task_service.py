from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


def create_task(
    db: Session,
    workflow_id: int,
    task_data: TaskCreate
):
    task = Task(
        name=task_data.name,
        workflow_id=workflow_id,
        priority=task_data.priority,
        max_retries=task_data.max_retries,
        timeout_seconds=task_data.timeout_seconds
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


def get_tasks(
    db: Session,
    workflow_id: int
):
    return (
        db.query(Task)
        .filter(Task.workflow_id == workflow_id)
        .all()
    )


def get_task(
    db: Session,
    task_id: int
):
    return (
        db.query(Task)
        .filter(Task.id == task_id)
        .first()
    )


def update_task(
    db: Session,
    task: Task,
    task_data: TaskUpdate
):
    if task_data.name is not None:
        task.name = task_data.name

    if task_data.priority is not None:
        task.priority = task_data.priority

    if task_data.max_retries is not None:
        task.max_retries = task_data.max_retries

    if task_data.timeout_seconds is not None:
        task.timeout_seconds = task_data.timeout_seconds

    db.commit()
    db.refresh(task)

    return task


def delete_task(
    db: Session,
    task: Task
):
    db.delete(task)
    db.commit()