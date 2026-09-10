from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.workflow import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
)
from app.services.workflow_service import (
    create_workflow,
    get_workflows,
    get_workflow,
    update_workflow,
    delete_workflow,
)


router = APIRouter(
    prefix="/workflows",
    tags=["Workflows"]
)


@router.post(
    "/",
    response_model=WorkflowResponse,
    status_code=201
)
def create_new_workflow(
    workflow_data: WorkflowCreate,
    db: Session = Depends(get_db)
):
    return create_workflow(db, workflow_data)


@router.get(
    "/",
    response_model=list[WorkflowResponse]
)
def list_workflows(
    db: Session = Depends(get_db)
):
    return get_workflows(db)


@router.get(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def get_single_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    workflow = get_workflow(db, workflow_id)

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return workflow


@router.put(
    "/{workflow_id}",
    response_model=WorkflowResponse
)
def update_existing_workflow(
    workflow_id: int,
    workflow_data: WorkflowUpdate,
    db: Session = Depends(get_db)
):
    workflow = get_workflow(db, workflow_id)

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    return update_workflow(
        db,
        workflow,
        workflow_data
    )


@router.delete(
    "/{workflow_id}",
    status_code=204
)
def delete_existing_workflow(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    workflow = get_workflow(db, workflow_id)

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found"
        )

    delete_workflow(db, workflow)

    return None