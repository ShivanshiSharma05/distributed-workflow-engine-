from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.enums import TaskStatus


class TaskExecutionStatusUpdate(BaseModel):
    status: TaskStatus


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