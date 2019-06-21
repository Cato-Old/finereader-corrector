from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class BeginItalicHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count - 1] == ' ':
            text_window.SendKeys('€', waitTime=0)
        return text, pass_count
