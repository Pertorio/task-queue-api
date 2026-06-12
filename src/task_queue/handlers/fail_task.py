from task_queue.handlers.base import TaskHandler

class FailTaskHandler(TaskHandler):
    async def execute(self, payload: dict) -> dict:
        raise RuntimeError(f"task execution failed internally")
        