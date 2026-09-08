from enum import Enum


class WorkflowStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DEAD_LETTER = "DEAD_LETTER"


class WorkerStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BUSY = "BUSY"
    UNHEALTHY = "UNHEALTHY"
    OFFLINE = "OFFLINE"