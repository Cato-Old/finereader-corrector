from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler
from app.mappings import SKR


class AbbreviationHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count:pass_count + 3] in SKR.keys():
            text_window.SendKeys('{Shift}({Right 3})', waitTime=0)
            char_abb = text[pass_count:pass_count + 3]
            text_window.SendKeys(SKR[char_abb], waitTime=0)
            text = text.replace(char_abb, SKR[char_abb], 1)
            pass_count += 1
        return text, pass_count
