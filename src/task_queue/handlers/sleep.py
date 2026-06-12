import asyncio
from task_queue.handlers.base import TaskHandler

class SleepHandler(TaskHandler):
    async def execute(self, payload: dict) -> dict:
        seconds = payload.get("seconds", 1)

        if not isinstance(seconds, (int, float)) or seconds < 0:
            raise ValueError(f"seconds must be a non-negative number, got: {seconds}")
        await asyncio.sleep(seconds)
        return {"slept_seconds": seconds}