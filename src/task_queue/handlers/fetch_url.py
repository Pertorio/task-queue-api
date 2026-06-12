import httpx
from task_queue.handlers.base import TaskHandler

class FetchURLHandler(TaskHandler):
    async def execute(self, payload: dict) -> dict:
        url = payload.get("url")
        if not url or not isinstance(url, str):
            raise ValueError(f"url must be a non-empty string, got: {url!r}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url=url)
            response.raise_for_status()
        return {
            "status_code": response.status_code,
            "content_length": len(response.content),
            "content_type": response.headers.get("content-type", "")
        }