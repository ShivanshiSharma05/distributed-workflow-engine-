from fastapi import APIRouter

from app.services.queue_service import (
    get_dead_letter_queue_length,
    get_dead_letter_tasks
)


router = APIRouter(
    prefix="/dead-letter-queue",
    tags=["Dead Letter Queue"]
)


@router.get("/")
def get_dead_letter_queue():
    return {
        "queue_name": "workflow_dead_letter_queue",
        "queue_length": get_dead_letter_queue_length(),
        "tasks": get_dead_letter_tasks()
    }