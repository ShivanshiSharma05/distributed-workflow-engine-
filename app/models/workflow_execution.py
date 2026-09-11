from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base
from app.models.enums import WorkflowStatus


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    status = Column(
        Enum(WorkflowStatus),
        default=WorkflowStatus.PENDING,
        nullable=False
    )

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    workflow = relationship(
        "Workflow",
        back_populates="executions"
    )

    task_executions = relationship(
        "TaskExecution",
        back_populates="workflow_execution",
        cascade="all, delete-orphan"
    )