from datetime import datetime

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