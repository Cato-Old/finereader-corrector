import time
from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.handler import Handler


class EndItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        text_window.SendKeys('{Left}', waitTime=0)
        offset = 1
        if text[pass_count-2] in (' ', '.', ','):
            text_window.SendKeys('{Left}', waitTime=0)
            offset += 1
        text_window.SendKeys(f'€{{Right {offset}}}', waitTime=0)
        while self.it_access.State == 16:
            time.sleep(0.001)
        return text, pass_count
