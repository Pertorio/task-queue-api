import asyncio
from task_queue.models.task import (
    Task, 
    TaskStatus,
    TaskType
)

# TaskStore (in-memory state)
# Store all the existing task
# Handle CRUD operations on Task - Create, Read, Update, Delete
# Thread-safe - Atomic (Handle multiple request with effecting data integrity)


class TaskStore:
    def __init__(self) -> None:
        self._tasks: dict[str, Task] = {}
        self._lock = asyncio.Lock()


    async def add(self, task: Task) -> None:
        async with self._lock:
            self._tasks[task.id] = task



    async def get(self, task_id: str) -> Task | None:
        async with self._lock:
            return self._tasks.get(task_id)
        

    async def list_all(
            self,
            status: TaskStatus | None = None,
            task_type: TaskType | None = None,
    ) -> list[Task]:
        async with self._lock:
            tasks = list(self._tasks.values())

        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if task_type is not None:
            tasks = [t for t in tasks if t.task_type == task_type]
        
        return tasks
    

    async def update(self, task: Task) -> None:
        async with self._lock:
            if task.id not in self._tasks:
                raise KeyError(f"Task {task.id} not found")
            self._tasks[task.id] = task

        
    


