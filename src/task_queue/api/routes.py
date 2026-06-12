from fastapi import APIRouter, Depends, HTTPException, Query, status

from task_queue.api.deps import get_store
from task_queue.core.store import TaskStore
from task_queue.models.schemas import TaskCreate, TaskResponse
from task_queue.models.task import Task, TaskStatus, TaskType

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def create_task(
    payload: TaskCreate,
    store: TaskStore = Depends(get_store),
    ) -> Task:
    """Submit a new task for background execution"""
    task = Task(task_type=payload.task_type, payload=payload.payload)
    await store.add(task)
    return task


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    store: TaskStore = Depends(get_store),
    ) -> Task:
    """Get a task by id"""
    task = await store.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task


@router.get("", response_model=list[TaskResponse])
async def list_tasks(
    task_status: TaskStatus | None = Query(default=None, alias="status"),
    task_type: TaskType | None = Query(default=None),
    store: TaskStore = Depends(get_store),
    ) -> list[Task]:
    """List tasks with optional filters"""
    return await store.list_all(status=task_status, task_type=task_type)


@router.delete("/{task_id}", response_model=TaskResponse)
async def cancel_task(
    task_id: str,
    store: TaskStore = Depends(get_store),
    ) -> Task:
    """Cancel a PENDING task. Returns 409 if task is already running."""
    task = await store.get(task_id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    if task.status != TaskStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot cancel task in status {task.status.value}",
        )

    task.status = TaskStatus.CANCELLED
    await store.update(task)
    return task