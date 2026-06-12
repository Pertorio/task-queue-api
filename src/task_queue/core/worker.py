import asyncio
import logging
from datetime import datetime, timezone

from task_queue.core.store import TaskStore
from task_queue.handlers import HANDLERS
from task_queue.models.task import Task, TaskStatus

logger = logging.getLogger(__name__)


class TaskWorker:
    def __init__(self, store: TaskStore, poll_interval: float = 0.1) -> None:
        self._store = store
        self._poll_interval = poll_interval
        self._running = False

    async def run(self) -> None:
        self._running = True
        logger.info("Worker started")

        while self._running:
            pending = await self._store.list_all(status=TaskStatus.PENDING)

            if not pending:
                await asyncio.sleep(self._poll_interval)
                continue

            task = pending[0]
            await self._process_task(task)

        logger.info("Worker stopped")

    def stop(self) -> None:
        self._running = False

    async def _process_task(self, task: Task) -> None:
        logger.info(f"Processing task {task.id} ({task.task_type})")

        # RUNNING
        task.status = TaskStatus.RUNNING
        task.updated_at = datetime.now(timezone.utc)
        await self._store.update(task)

        # Execute
        try:
            handler = HANDLERS[task.task_type]
            result = await handler.execute(task.payload)

            # COMPLETED
            task.status = TaskStatus.COMPLETED
            task.result = result
            logger.info(f"Task {task.id} completed")

        except Exception as e:
            # FAILED
            task.status = TaskStatus.FAILED
            task.error = str(e)
            logger.warning(f"Task {task.id} failed: {e}")

        # Final update
        task.updated_at = datetime.now(timezone.utc)
        await self._store.update(task)