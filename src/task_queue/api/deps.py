from task_queue.core.store import TaskStore
from task_queue.core.worker import TaskWorker

_store = TaskStore()
_worker = TaskWorker(store=_store)


def get_store() -> TaskStore:
    return _store


def get_worker() -> TaskWorker:
    return _worker