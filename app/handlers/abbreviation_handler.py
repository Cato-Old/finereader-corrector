import time

from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.handler import Handler
from app.mappings import SKR


class AbbreviationHandler(Handler):

    def __init__(self, italic: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[0:3] in SKR.keys():
            text_window.SendKeys('{Shift}({Right 3})', waitTime=0)
            char_abb = text_pos[0:3]
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
            text_pos.text = text_pos.text.replace(char_abb, SKR[char_abb], 1)
            text_pos += 1
        return text_pos
