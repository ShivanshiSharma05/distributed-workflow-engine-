from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
from app.models.enums import WorkflowStatus


class WorkflowExecution(Base):
    __tablename__ = "workflow_executions"

    id = Column(Integer, primary_key=True, index=True)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False
    )

    status = Column(
        Enum(WorkflowStatus),
        default=WorkflowStatus.PENDING,
        nullable=False
    )

    started_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    completed_at = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
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