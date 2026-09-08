from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Enum,
    Text
)

from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
from app.models.enums import TaskStatus


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True, index=True)

    workflow_execution_id = Column(
        Integer,
        ForeignKey("workflow_executions.id", ondelete="CASCADE"),
        nullable=False
    )

    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    status = Column(
        Enum(TaskStatus),
        default=TaskStatus.PENDING,
        nullable=False
    )

    retry_count = Column(Integer, default=0)

    worker_id = Column(
        Integer,
        ForeignKey("workers.id", ondelete="SET NULL"),
        nullable=True
    )

    started_at = Column(DateTime(timezone=True), nullable=True)

    completed_at = Column(DateTime(timezone=True), nullable=True)

    error_message = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    workflow_execution = relationship(
        "WorkflowExecution",
        back_populates="task_executions"
    )

    task = relationship(
        "Task",
        back_populates="executions"
    )

    worker = relationship(
        "Worker",
        back_populates="task_executions"
    )