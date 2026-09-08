from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.sql import func

from app.db.database import Base


class ExecutionEvent(Base):
    __tablename__ = "execution_events"

    id = Column(Integer, primary_key=True, index=True)

    workflow_execution_id = Column(
        Integer,
        ForeignKey("workflow_executions.id", ondelete="CASCADE"),
        nullable=False
    )

    task_execution_id = Column(
        Integer,
        ForeignKey("task_executions.id", ondelete="CASCADE"),
        nullable=True
    )

    event_type = Column(
        String(100),
        nullable=False
    )

    message = Column(
        String(1000),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )