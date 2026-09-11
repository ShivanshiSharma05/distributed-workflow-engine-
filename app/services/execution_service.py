from datetime import datetime

from sqlalchemy.orm import Session

from app.models.workflow import Workflow
from app.models.task import Task
from app.models.workflow_execution import WorkflowExecution
from app.models.task_execution import TaskExecution
from app.models.enums import WorkflowStatus, TaskStatus


def get_workflow(
    db: Session,
    workflow_id: int
):
    return (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )


def get_execution(
    db: Session,
    execution_id: int
):
    return (
        db.query(WorkflowExecution)
        .filter(
            WorkflowExecution.id == execution_id
        )
        .first()
    )


def create_workflow_execution(
    db: Session,
    workflow_id: int
):
    workflow = get_workflow(db, workflow_id)

    if workflow is None:
        raise ValueError("Workflow not found.")

    tasks = (
        db.query(Task)
        .filter(Task.workflow_id == workflow_id)
        .all()
    )

    if not tasks:
        raise ValueError(
            "Cannot execute a workflow without tasks."
        )

    execution = WorkflowExecution(
        workflow_id=workflow_id,
        status=WorkflowStatus.PENDING
    )

    db.add(execution)
    db.flush()

    for task in tasks:
        task_execution = TaskExecution(
            workflow_execution_id=execution.id,
            task_id=task.id,
            status=TaskStatus.PENDING,
            retry_count=0
        )

        db.add(task_execution)

    db.commit()
    db.refresh(execution)

    return execution


def get_executions(
    db: Session,
    workflow_id: int
):
    return (
        db.query(WorkflowExecution)
        .filter(
            WorkflowExecution.workflow_id == workflow_id
        )
        .order_by(
            WorkflowExecution.created_at.desc()
        )
        .all()
    )


def get_execution_details(
    db: Session,
    execution_id: int
):
    return get_execution(db, execution_id)


def start_execution(
    db: Session,
    execution: WorkflowExecution
):
    execution.status = WorkflowStatus.RUNNING
    execution.started_at = datetime.utcnow()

    db.commit()
    db.refresh(execution)

    return execution