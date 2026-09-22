from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.execution import (
    WorkflowExecutionCreate,
    WorkflowExecutionResponse,
    WorkflowExecutionDetailResponse,
    ExecutionSummaryResponse
)

from app.services import execution_service


router = APIRouter(
    prefix="/executions",
    tags=["Executions"]
)


# =========================================================
# 1. CREATE WORKFLOW EXECUTION
# =========================================================

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
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


# =========================================================
# 2. GET ALL EXECUTIONS FOR A WORKFLOW
# =========================================================

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workflow not found."
        )

    return execution_service.get_executions(
        db,
        workflow_id
    )


# =========================================================
# 3. GET EXECUTION DETAILS
# =========================================================

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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found."
        )

    return execution


# =========================================================
# 4. GET EXECUTION SUMMARY
# =========================================================

@router.get(
    "/{execution_id}/summary",
    response_model=ExecutionSummaryResponse
)
def execution_summary(
    execution_id: int,
    db: Session = Depends(get_db)
):
    summary = execution_service.get_execution_summary(
        db,
        execution_id
    )

    if summary is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found."
        )

    return summary