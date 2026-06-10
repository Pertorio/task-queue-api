from pydantic import BaseModel, Field
from datetime import datetime
from task_queue.models.task import (
    TaskStatus,
    TaskType
)

class TaskCreate(BaseModel):
    task_type: TaskType
    payload: dict = Field(default_factory=dict)


class TaskResponse(BaseModel):
    id: str
    task_type: TaskType
    status: TaskStatus
    payload: dict
    result: dict | None
    error: str | None
    created_at: datetime
    updated_at: datetime
    model_config = {"from_attributes": True}