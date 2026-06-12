from task_queue.handlers.base import TaskHandler
from task_queue.handlers.fail_task import FailTaskHandler
from task_queue.handlers.fetch_url import FetchURLHandler
from task_queue.handlers.multiply import MultiplyHandler
from task_queue.handlers.sleep import SleepHandler
from task_queue.models.task import TaskType


HANDLERS: dict[TaskType, TaskHandler] = {
    TaskType.SLEEP: SleepHandler(),
    TaskType.MULTIPLY: MultiplyHandler(),
    TaskType.FETCH_URL: FetchURLHandler(),
    TaskType.FAIL_TASK: FailTaskHandler(),
}