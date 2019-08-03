from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class InternalItalicHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        while self.it_access.State == 16:
            text_pos = self.abb_hdl.handle(text_window, text_pos)
            text_window.SendKeys('{Right}', waitTime=0)
            text_pos += 1

            if text_pos.pos >= len(text_pos.text) or text_pos[0] == '\n':
                self.it_invoke.Invoke()
                break

        return text_pos
