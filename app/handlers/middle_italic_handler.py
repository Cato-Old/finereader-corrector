from uiautomation import PaneControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class MiddleItalicHandler(Handler):

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        stop_chars = (' ', '(', '=', '>', '\t', '\n', '_', '[')
        if text_pos[-1] not in stop_chars:
            while text_pos[-1] not in stop_chars:
                text_window.SendKeys('{Left}', waitTime=0)
                text_pos -= 1
        return text_pos
