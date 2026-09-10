from sqlalchemy.orm import Session

from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate


def create_workflow(
    db: Session,
    workflow_data: WorkflowCreate
):
    workflow = Workflow(
        name=workflow_data.name,
        description=workflow_data.description
    )

    db.add(workflow)
    db.commit()
    db.refresh(workflow)

    return workflow


def get_workflows(db: Session):
    return db.query(Workflow).all()


def get_workflow(
    db: Session,
    workflow_id: int
):
    return (
        db.query(Workflow)
        .filter(Workflow.id == workflow_id)
        .first()
    )


def update_workflow(
    db: Session,
    workflow: Workflow,
    workflow_data: WorkflowUpdate
):
    if workflow_data.name is not None:
        workflow.name = workflow_data.name

    if workflow_data.description is not None:
        workflow.description = workflow_data.description

    db.commit()
    db.refresh(workflow)

    return workflow


def delete_workflow(
    db: Session,
    workflow: Workflow
):
    db.delete(workflow)
    db.commit()