import time
from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class BeginItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count - 1] in (' ', '>', '('):
            text_window.SendKeys('€', waitTime=0)
            text, pass_count = self.abb_hdl.handle(text_window,
                                                   text, pass_count)
            text_window.SendKeys('{Right}', waitTime=0)
            pass_count += 1
            while self.it_access.State == 0:
                time.sleep(0.001)
        return text, pass_count
