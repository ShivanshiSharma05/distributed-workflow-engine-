from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.execution import (
    WorkflowExecutionCreate,
    WorkflowExecutionResponse,
    WorkflowExecutionDetailResponse
)

from app.services import execution_service


router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)


@router.post(
    "/",
    response_model=WorkflowExecutionResponse,
    status_code=status.HTTP_201_CREATED
)
def create_execution(
    execution_data: WorkflowExecutionCreate,
    db: Session = Depends(get_db)
):
    try:
        execution = execution_service.create_workflow_execution(
            db,
            execution_data.workflow_id
        )

        return execution

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/workflow/{workflow_id}",
    response_model=list[WorkflowExecutionResponse]
)
def get_workflow_executions(
    workflow_id: int,
    db: Session = Depends(get_db)
):
    workflow = execution_service.get_workflow(
        db,
        workflow_id
    )

    if workflow is None:
        raise HTTPException(
            status_code=404,
            detail="Workflow not found."
        )

    return execution_service.get_executions(
        db,
        workflow_id
    )


@router.get(
    "/{execution_id}",
    response_model=WorkflowExecutionDetailResponse
)
def get_execution(
    execution_id: int,
    db: Session = Depends(get_db)
):
    execution = execution_service.get_execution_details(
        db,
        execution_id
    )

    if execution is None:
        raise HTTPException(
            status_code=404,
            detail="Execution not found."
        )

    return execution