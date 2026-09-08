from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.database import Base
from app.models.enums import WorkerStatus


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)

    worker_name = Column(
        String(255),
        unique=True,
        nullable=False
    )

    status = Column(
        Enum(WorkerStatus),
        default=WorkerStatus.ACTIVE,
        nullable=False
    )

    last_heartbeat = Column(
        DateTime(timezone=True),
        nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    task_executions = relationship(
        "TaskExecution",
        back_populates="worker"
    )