from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from app.models.enums import TaskStatus


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True, index=True)

    workflow_execution_id = Column(
        Integer,
        ForeignKey("workflow_executions.id"),
        nullable=False
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id"),
        nullable=False
    )

    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )

    retry_count = Column(
        Integer,
        default=0
    )

    worker_id = Column(
        Integer,
        ForeignKey("workers.id"),
        nullable=True
    )

    started_at = Column(DateTime, nullable=True)

    completed_at = Column(
        DateTime,
        nullable=True
    )

    error_message = Column(
        Text,
        nullable=True
    )

    workflow_execution = relationship(
        "WorkflowExecution",
        back_populates="task_executions"
    )

    task = relationship("Task")

    worker = relationship(
        "Worker",
        back_populates="task_executions"
    )