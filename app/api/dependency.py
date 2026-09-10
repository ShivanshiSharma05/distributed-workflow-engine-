from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.task_dependency import TaskDependency
from app.schemas.dependency import (
    DependencyCreate,
    DependencyResponse
)
from app.services import dependency_service


router = APIRouter(
    prefix="/dependencies",
    tags=["Dependencies"]
)


@router.post(
    "/",
    response_model=DependencyResponse,
    status_code=status.HTTP_201_CREATED
)
def create_dependency(
    dependency_data: DependencyCreate,
    db: Session = Depends(get_db)
):
    try:
        dependency = dependency_service.create_dependency(
            db,
            dependency_data.task_id,
            dependency_data.depends_on_task_id
        )

        return dependency

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )


@router.get(
    "/task/{task_id}",
    response_model=list[DependencyResponse]
)
def get_task_dependencies(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = dependency_service.get_task(db, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found."
        )

    return dependency_service.get_dependencies(
        db,
        task_id
    )


@router.delete(
    "/{dependency_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_dependency(
    dependency_id: int,
    db: Session = Depends(get_db)
):
    dependency = dependency_service.delete_dependency(
        db,
        dependency_id
    )

    if dependency is None:
        raise HTTPException(
            status_code=404,
            detail="Dependency not found."
        )

    return None