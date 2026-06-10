from enum import Enum
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class TaskType(str, Enum):
    SLEEP = "sleep"
    MULTIPLY = "multiply"
    FETCH_URL = "fetch_url"
    FAIL_TASK = "fail_task"

@dataclass
class Task:
    task_type: TaskType
    payload: dict

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: TaskStatus =field(default=TaskStatus.PENDING)
    result: dict | None = field(default=None)
    error: str | None = field(default=None)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))