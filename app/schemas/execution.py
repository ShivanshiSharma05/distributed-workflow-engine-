from datetime import datetime
from typing import Dict

from pydantic import BaseModel, ConfigDict

from app.models.enums import WorkflowStatus, TaskStatus


class WorkflowExecutionCreate(BaseModel):
    workflow_id: int


class TaskExecutionResponse(BaseModel):
    id: int
    workflow_execution_id: int
    task_id: int
    status: TaskStatus
    retry_count: int
    worker_id: int | None
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None

    model_config = ConfigDict(from_attributes=True)


class WorkflowExecutionResponse(BaseModel):
    id: int
    workflow_id: int
    status: WorkflowStatus
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)


class WorkflowExecutionDetailResponse(WorkflowExecutionResponse):
    task_executions: list[TaskExecutionResponse] = []


class ExecutionSummaryResponse(BaseModel):
    execution_id: int
    workflow_id: int
    workflow_status: str

    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime | None

    total_tasks: int
    completed_tasks: int

    pending_tasks: int
    ready_tasks: int
    queued_tasks: int
    running_tasks: int
    success_tasks: int
    failed_tasks: int
    retrying_tasks: int
    dead_letter_tasks: int

    task_status_counts: Dict[str, int]    