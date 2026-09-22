
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
    """
    Create a workflow execution and create one
    TaskExecution record for every task.
    """

    workflow = get_workflow(
        db,
        workflow_id
    )

    if workflow is None:
        raise ValueError(
            "Workflow not found."
        )

    tasks = (
        db.query(Task)
        .filter(
            Task.workflow_id == workflow_id
        )
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

    # Generate the execution ID before creating
    # the associated task executions.
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
    """
    Return all executions for a workflow.
    """

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
    """
    Return details of one workflow execution.
    """

    return get_execution(
        db,
        execution_id
    )


def start_execution(
    db: Session,
    execution: WorkflowExecution
):
    """
    Mark a workflow execution as RUNNING.
    """

    execution.status = WorkflowStatus.RUNNING

    if execution.started_at is None:
        execution.started_at = datetime.utcnow()

    db.commit()
    db.refresh(execution)

    return execution


def update_workflow_status(
    db: Session,
    workflow_execution_id: int
):
    """
    Calculate the workflow status from all task
    execution statuses.

    Rules:

    1. All tasks SUCCESS -> Workflow SUCCESS
    2. Any task FAILED or DEAD_LETTER -> Workflow FAILED
    3. Any active task -> Workflow RUNNING
    """

    execution = get_execution(
        db,
        workflow_execution_id
    )

    if execution is None:
        return None

    task_executions = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id
            == workflow_execution_id
        )
        .all()
    )

    if not task_executions:
        return execution

    all_success = all(
        task_execution.status == TaskStatus.SUCCESS
        for task_execution in task_executions
    )

    any_failed = any(
        task_execution.status in (
            TaskStatus.FAILED,
            TaskStatus.DEAD_LETTER
        )
        for task_execution in task_executions
    )

    has_active_tasks = any(
        task_execution.status in (
            TaskStatus.PENDING,
            TaskStatus.READY,
            TaskStatus.QUEUED,
            TaskStatus.RUNNING,
            TaskStatus.RETRYING
        )
        for task_execution in task_executions
    )

    if all_success:
        execution.status = WorkflowStatus.SUCCESS

        if execution.started_at is None:
            execution.started_at = datetime.utcnow()

        if execution.completed_at is None:
            execution.completed_at = datetime.utcnow()

    elif any_failed:
        execution.status = WorkflowStatus.FAILED

        if execution.started_at is None:
            execution.started_at = datetime.utcnow()

        if execution.completed_at is None:
            execution.completed_at = datetime.utcnow()

    elif has_active_tasks:
        execution.status = WorkflowStatus.RUNNING

        if execution.started_at is None:
            execution.started_at = datetime.utcnow()

    db.commit()
    db.refresh(execution)

    return execution


def get_execution_summary(
    db: Session,
    execution_id: int
):
    """
    Recalculate workflow status and return a complete
    execution summary.

    Recalculating here also fixes old executions whose
    workflow status was not updated during task processing.
    """

    execution = update_workflow_status(
        db,
        execution_id
    )

    if execution is None:
        return None

    task_executions = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id
            == execution_id
        )
        .all()
    )

    status_counts = {
        "PENDING": 0,
        "READY": 0,
        "QUEUED": 0,
        "RUNNING": 0,
        "SUCCESS": 0,
        "FAILED": 0,
        "RETRYING": 0,
        "DEAD_LETTER": 0
    }

    for task_execution in task_executions:
        status = task_execution.status

        if hasattr(status, "value"):
            status = status.value

        if status in status_counts:
            status_counts[status] += 1

    total_tasks = len(task_executions)

    completed_tasks = (
        status_counts["SUCCESS"]
        + status_counts["FAILED"]
        + status_counts["DEAD_LETTER"]
    )

    workflow_status = execution.status

    if hasattr(workflow_status, "value"):
        workflow_status = workflow_status.value

    return {
        "execution_id": execution.id,
        "workflow_id": execution.workflow_id,
        "workflow_status": workflow_status,

        "started_at": execution.started_at,
        "completed_at": execution.completed_at,
        "created_at": execution.created_at,

        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,

        "pending_tasks": status_counts["PENDING"],
        "ready_tasks": status_counts["READY"],
        "queued_tasks": status_counts["QUEUED"],
        "running_tasks": status_counts["RUNNING"],
        "success_tasks": status_counts["SUCCESS"],
        "failed_tasks": status_counts["FAILED"],
        "retrying_tasks": status_counts["RETRYING"],
        "dead_letter_tasks": status_counts["DEAD_LETTER"],

        "task_status_counts": status_counts
    }