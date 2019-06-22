import time
from typing import Tuple

from uiautomation import PaneControl, ButtonControl

from app.handlers.handler import Handler
from app.mappings import SKR


class AbbreviationHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count:pass_count + 3] in SKR.keys():
            text_window.SendKeys('{Shift}({Right 3})', waitTime=0)
            char_abb = text[pass_count:pass_count + 3]
            is_italic = self.it_access.State == 16
            text_window.SendKeys(SKR[char_abb], waitTime=0)
            while self.it_access.State == 16:
                time.sleep(0.001)
            if is_italic:
                text_window.SendKeys('{Shift}({Left})', waitTime=0)
                self.it_invoke.Invoke()
                text_window.SendKeys('{Right}', waitTime=0)
                while self.it_access.State == 0:
                    time.sleep(0.001)
            text = text.replace(char_abb, SKR[char_abb], 1)
            pass_count += 1
        return text, pass_count
