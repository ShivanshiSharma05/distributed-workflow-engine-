from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(255), nullable=False)

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False
    )

    priority = Column(Integer, default=5)

    max_retries = Column(Integer, default=3)

    timeout_seconds = Column(Integer, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    workflow = relationship(
        "Workflow",
        back_populates="tasks"
    )

    executions = relationship(
        "TaskExecution",
        back_populates="task",
        cascade="all, delete-orphan"
    )