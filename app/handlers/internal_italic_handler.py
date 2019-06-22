from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class InternalItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        while self.it_access.State == 16:
            text, pass_count = self.abb_hdl.handle(text_window,
                                                   text, pass_count)
            text_window.SendKeys('{Right}', waitTime=0)
            pass_count += 1

            if pass_count >= len(text):
                self.it_invoke.Invoke()
                text_window.SendKeys('€', waitTime=0.01)
                break
        return text, pass_count
