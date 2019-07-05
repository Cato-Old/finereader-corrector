import time
from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.handler import Handler


class EndItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        text_window.SendKeys('{Left}', waitTime=0)
        offset = self.__set_offset(text, pass_count)
        text_window.SendKeys(f'{{Shift}}({{Left {offset}}})', waitTime=0)
        self.it_invoke.Invoke(waitTime=0)
        if offset > 0:
            text_window.SendKeys('{Left}', waitTime=0)
            self.it_invoke.Invoke(waitTime=0)
        text_window.SendKeys(f'€{{Right {offset}}}', waitTime=0)
        while self.it_access.State == 16:
            time.sleep(0.001)
        return text, pass_count - 1

    @staticmethod
    def __set_offset(text: str, pass_count: int) -> int:
        if text[pass_count - 3:pass_count - 1] in ('. ', ', '):
            return 2
        elif text[pass_count - 3:pass_count - 1] in ('..'):
            return 0
        elif text[pass_count - 2] in (' ', '.', ',', '|', '\n'):
            return 1
        else:
            return 0
