from abc import ABC, abstractmethod
from typing import Tuple

from uiautomation import PaneControl

from app.cursor import TextPosition


class Handler(ABC):

    @abstractmethod
    def handle(self,
               text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        pass
