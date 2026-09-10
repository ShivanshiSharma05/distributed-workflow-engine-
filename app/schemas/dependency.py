from pydantic import BaseModel


class DependencyCreate(BaseModel):
    task_id: int
    depends_on_task_id: int


class DependencyResponse(BaseModel):
    id: int
    task_id: int
    depends_on_task_id: int

    class Config:
        from_attributes = True