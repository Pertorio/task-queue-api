from task_queue.handlers.base import TaskHandler

class MultiplyHandler(TaskHandler):
    async def execute(self, payload: dict) -> dict:
        if "a" not in payload or "b" not in payload:
            raise ValueError(f"payload must cotain 'a' and 'b'")
        
        a = payload["a"]
        b = payload["b"]

        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise ValueError(f"a and b must be numbers, got: a={a!r}, b={b!r}")
        
        return {"product": a*b}