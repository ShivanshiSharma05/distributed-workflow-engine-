from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint

from app.db.database import Base


class TaskDependency(Base):
    __tablename__ = "task_dependencies"

    id = Column(Integer, primary_key=True)

    task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    depends_on_task_id = Column(
        Integer,
        ForeignKey("tasks.id", ondelete="CASCADE"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "depends_on_task_id",
            name="unique_task_dependency"
        ),
    )