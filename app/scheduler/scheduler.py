from sqlalchemy.orm import Session

from app.models.task_dependency import TaskDependency
from app.models.task_execution import TaskExecution
from app.models.enums import TaskStatus


def get_task_dependencies(
    db: Session,
    task_id: int
):
    return (
        db.query(TaskDependency)
        .filter(
            TaskDependency.task_id == task_id
        )
        .all()
    )


def get_dependency_status(
    db: Session,
    workflow_execution_id: int,
    dependency_task_id: int
):
    return (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id == workflow_execution_id,
            TaskExecution.task_id == dependency_task_id
        )
        .first()
    )


def is_task_ready(
    db: Session,
    workflow_execution_id: int,
    task_id: int
):
    dependencies = get_task_dependencies(
        db,
        task_id
    )

    # No dependencies → task is immediately ready
    if not dependencies:
        return True

    for dependency in dependencies:

        dependency_execution = get_dependency_status(
            db,
            workflow_execution_id,
            dependency.depends_on_task_id
        )

        # Dependency execution does not exist
        if dependency_execution is None:
            return False

        # Dependency must be SUCCESS
        if dependency_execution.status != TaskStatus.SUCCESS:
            return False

    return True


def get_ready_tasks(
    db: Session,
    workflow_execution_id: int
):
    task_executions = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id == workflow_execution_id
        )
        .all()
    )

    ready_tasks = []

    for task_execution in task_executions:

        # Only PENDING tasks can become READY
        if task_execution.status != TaskStatus.PENDING:
            continue

        if is_task_ready(
            db,
            workflow_execution_id,
            task_execution.task_id
        ):
            task_execution.status = TaskStatus.READY
            ready_tasks.append(task_execution)

    db.commit()

    return ready_tasks