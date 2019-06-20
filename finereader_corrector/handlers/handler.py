from abc import ABC, abstractmethod
from typing import Tuple

from uiautomation import PaneControl


class Handler(ABC):

    @abstractmethod
    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        pass
