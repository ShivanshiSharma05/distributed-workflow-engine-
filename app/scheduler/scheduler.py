from sqlalchemy.orm import Session

from app.models.task_dependency import TaskDependency
from app.models.task_execution import TaskExecution
from app.models.task import Task
from app.models.enums import TaskStatus


# ---------------------------------------------------------
# GET TASK DEPENDENCIES
# ---------------------------------------------------------

def get_task_dependencies(db: Session, task_id: int):
    """
    Get all dependencies of a task.

    Example:
        Task B depends on Task A

    task_id = B
    depends_on_task_id = A
    """

    return (
        db.query(TaskDependency)
        .filter(
            TaskDependency.task_id == task_id
        )
        .all()
    )


# ---------------------------------------------------------
# GET DEPENDENCY EXECUTION STATUS
# ---------------------------------------------------------

def get_dependency_status(
    db: Session,
    workflow_execution_id: int,
    dependency_task_id: int
):
    """
    Get the execution record of a dependency
    inside the current workflow execution.
    """

    return (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id
            == workflow_execution_id,

            TaskExecution.task_id
            == dependency_task_id
        )
        .first()
    )


# ---------------------------------------------------------
# CHECK WHETHER TASK IS READY
# ---------------------------------------------------------

def is_task_ready(
    db: Session,
    workflow_execution_id: int,
    task_id: int
):
    """
    A task is READY when all of its dependencies
    have completed successfully.
    """

    dependencies = get_task_dependencies(
        db,
        task_id
    )

    # No dependencies → task can run immediately
    if not dependencies:
        return True

    # Check every dependency
    for dependency in dependencies:

        dependency_execution = get_dependency_status(
            db,
            workflow_execution_id,
            dependency.depends_on_task_id
        )

        # Dependency execution does not exist
        if dependency_execution is None:
            return False

        # Dependency has not succeeded
        if dependency_execution.status != TaskStatus.SUCCESS:
            return False

    # All dependencies succeeded
    return True


# ---------------------------------------------------------
# GET READY TASKS WITH PRIORITY
# ---------------------------------------------------------

def get_ready_tasks(
    db: Session,
    workflow_execution_id: int
):
    """
    Find all PENDING tasks whose dependencies
    have completed successfully.

    READY tasks are sorted by priority.

    Higher priority number = higher priority.

    Example:
        Task A → priority 2
        Task B → priority 10
        Task C → priority 5

    Result:
        B → C → A
    """

    # Get all task executions for this workflow execution
    task_executions = (
        db.query(TaskExecution)
        .filter(
            TaskExecution.workflow_execution_id
            == workflow_execution_id
        )
        .all()
    )

    ready_tasks = []

    # -----------------------------------------------------
    # Find tasks that are ready
    # -----------------------------------------------------

    for task_execution in task_executions:

        # Only PENDING tasks need readiness checking
        if task_execution.status != TaskStatus.PENDING:
            continue

        # Check dependencies
        if is_task_ready(
            db,
            workflow_execution_id,
            task_execution.task_id
        ):

            # Mark task as READY
            task_execution.status = TaskStatus.READY

            # Get original task definition
            task = (
                db.query(Task)
                .filter(
                    Task.id == task_execution.task_id
                )
                .first()
            )

            # Get priority
            priority = task.priority if task else 0

            # Store task + priority
            ready_tasks.append(
                (
                    task_execution,
                    priority
                )
            )

    # -----------------------------------------------------
    # Sort by priority
    # -----------------------------------------------------
    #
    # Higher number = higher priority
    #
    # Example:
    # 10
    # 7
    # 3
    # 1
    #
    # -----------------------------------------------------

    ready_tasks.sort(
        key=lambda item: item[1],
        reverse=True
    )

    # Save READY status changes
    db.commit()

    # Return only TaskExecution objects
    return [
        task_execution
        for task_execution, priority
        in ready_tasks
    ]