from abc import ABC, abstractmethod

class TaskHandler(ABC):
    @abstractmethod
    async def execute(self, payload: dict) -> dict:
        ...