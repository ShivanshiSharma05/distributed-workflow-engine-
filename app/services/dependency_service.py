from sqlalchemy.orm import Session

from app.models.task import Task
from app.models.task_dependency import TaskDependency


def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


def dependency_exists(
    db: Session,
    task_id: int,
    depends_on_task_id: int
):
    return (
        db.query(TaskDependency)
        .filter(
            TaskDependency.task_id == task_id,
            TaskDependency.depends_on_task_id == depends_on_task_id
        )
        .first()
    )


def creates_cycle(
    db: Session,
    task_id: int,
    depends_on_task_id: int
):
    """
    Check whether adding:

        depends_on_task_id -> task_id

    would create a cycle.
    """

    visited = set()
    stack = [task_id]

    while stack:

        current_task = stack.pop()

        if current_task == depends_on_task_id:
            return True

        if current_task in visited:
            continue

        visited.add(current_task)

        dependencies = (
            db.query(TaskDependency)
            .filter(
                TaskDependency.task_id == current_task
            )
            .all()
        )

        for dependency in dependencies:
            stack.append(dependency.depends_on_task_id)

    return False


def create_dependency(
    db: Session,
    task_id: int,
    depends_on_task_id: int
):
    if task_id == depends_on_task_id:
        raise ValueError("A task cannot depend on itself.")

    task = get_task(db, task_id)
    depends_on_task = get_task(db, depends_on_task_id)

    if task is None:
        raise ValueError("Task does not exist.")

    if depends_on_task is None:
        raise ValueError("Dependency task does not exist.")

    if task.workflow_id != depends_on_task.workflow_id:
        raise ValueError(
            "Tasks must belong to the same workflow."
        )

    if dependency_exists(
        db,
        task_id,
        depends_on_task_id
    ):
        raise ValueError(
            "This dependency already exists."
        )

    if creates_cycle(
        db,
        task_id,
        depends_on_task_id
    ):
        raise ValueError(
            "This dependency would create a cycle."
        )

    dependency = TaskDependency(
        task_id=task_id,
        depends_on_task_id=depends_on_task_id
    )

    db.add(dependency)
    db.commit()
    db.refresh(dependency)

    return dependency


def get_dependencies(
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


def delete_dependency(
    db: Session,
    dependency_id: int
):
    dependency = (
        db.query(TaskDependency)
        .filter(
            TaskDependency.id == dependency_id
        )
        .first()
    )

    if dependency is None:
        return None

    db.delete(dependency)
    db.commit()

    return dependency