from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class BeginItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count - 1] == ' ':
            text_window.SendKeys('€', waitTime=0)
            text, pass_count = self.abb_hdl.handle(text_window,
                                                   text, pass_count)
            text_window.SendKeys('{Right}', waitTime=0)
            pass_count += 1
        return text, pass_count
