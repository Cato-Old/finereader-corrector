import time

from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class EndItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        text_window.SendKeys('{Left}', waitTime=0)
        offset = self.__set_offset(text_pos)
        text_window.SendKeys(f'{{Shift}}({{Left {offset}}})', waitTime=0)
        self.it_invoke.Invoke(waitTime=0)
        if offset > 0:
            text_window.SendKeys('{Left}', waitTime=0)
        text_window.SendKeys(f'€{{Right {offset}}}', waitTime=0)
        while self.it_access.State == 16:
            time.sleep(0.001)
        return text_pos - 1

    @staticmethod
    def __set_offset(text_pos: TextPosition) -> int:
        if text_pos[-3:-1] in ('. ', ', '):
            return 2
        elif text_pos[-3:-1] in ('..'):
            return 0
        elif text_pos[-2] in (' ', '.', ',', '|', '\n'):
            return 1
        else:
            return 0
