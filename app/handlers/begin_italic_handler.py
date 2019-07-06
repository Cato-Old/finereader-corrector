import time
from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class BeginItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        text_pos = TextPosition(text, pass_count)
        if text_pos[-1] in (' ', '>', '('):
            text_window.SendKeys('€', waitTime=0)
            text, pass_count = self.abb_hdl.handle(text_window, text_pos.text,
                                                   text_pos.pos)
            text_window.SendKeys('{Right}', waitTime=0)
            text_pos = TextPosition(text, pass_count)
            text_pos = text_pos + 1
            while self.it_access.State == 0:
                time.sleep(0.001)
        return text_pos.text, text_pos.pos
