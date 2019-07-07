from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class MiddleItalicHandler(Handler):

    def __init__(self, italic: ButtonControl) -> None:
        self.it_access = italic.GetLegacyIAccessiblePattern()

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        stop_chars = (' ', '(', '=', '>', '\t', '\n', '_', '[')
        while text_pos[-1] not in stop_chars or self.it_access.State != 0:
            text_window.SendKeys('{Left}', waitTime=0)
            text_pos -= 1
        return text_pos
