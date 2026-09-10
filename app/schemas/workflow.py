from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkflowCreate(BaseModel):
    name: str
    description: str | None = None


class WorkflowUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime | None
    updated_at: datetime | None

    model_config = ConfigDict(from_attributes=True)