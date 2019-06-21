from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class MiddleItalicHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        stop_chars = (' ', '(', '=', '>', '\t', '\n', '_', '[')
        if pass_count > 1 and not text[pass_count - 1] in stop_chars:
            while not text[pass_count - 1] in stop_chars:
                text_window.SendKeys('{Left}', waitTime=0)
                pass_count -= 1
        return text, pass_count
