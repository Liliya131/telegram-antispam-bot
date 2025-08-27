from queue import Queue, Empty
from typing import Any, Optional


class DelayedResponseQueue(Queue):
    """
    One-shot queue:
    - принимает ровно один элемент,
    - после получения элемента очередь закрывается,
    - повторные put/get невозможны.
    """
    def __init__(self) -> None:
        super().__init__(maxsize=1)
        self._closed = False

    def put(self, item: Any, block: bool = True, timeout: Optional[float] = None) -> None:
        if self._closed:
            raise RuntimeError("Queue is closed")
        super().put(item, block, timeout)

    def get(self, block: bool = True, timeout: Optional[float] = None) -> Any:
        if self._closed:
            raise RuntimeError("Queue is closed")
        try:
            result = super().get(block, timeout)
            self.task_done()
            self._closed = True
            return result
        except Empty:
            raise
