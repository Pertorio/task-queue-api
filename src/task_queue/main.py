import asyncio

from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from task_queue.api.deps import get_worker
from task_queue.api.routes import router
from task_queue.config import settings
from task_queue.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Manage worker lifecycle alongside the FastAPI app"""
    logger.info("app_starting", host=settings.host, port=settings.port)

    worker = get_worker()
    worker_task = asyncio.create_task(worker.run())

    yield

    logger.info("app_stopping")
    worker.stop()
    await worker_task
    logger.info("app_stopped")


app = FastAPI(
    title="Task Queue API",
    description="Async task queue REST API built with FastAPI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health() -> dict:
    """Health check endpoint"""
    return {"status": "ok"}