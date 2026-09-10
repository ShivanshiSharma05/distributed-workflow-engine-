from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskCreate(BaseModel):
    name: str
    priority: int = 5
    max_retries: int = 3
    timeout_seconds: int | None = None


class TaskUpdate(BaseModel):
    name: str | None = None
    priority: int | None = None
    max_retries: int | None = None
    timeout_seconds: int | None = None


class TaskResponse(BaseModel):
    id: int
    name: str
    workflow_id: int
    priority: int
    max_retries: int
    timeout_seconds: int | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)