import time
from typing import Tuple

import pyperclip
from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.handler import Handler


class BeginItalicHandler(Handler):

    def __init__(self, italic: ButtonControl,
                 copy_button_control: ButtonControl):
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.copy_button_control = copy_button_control
        self.abb_hdl = AbbreviationHandler(italic)

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[-4:-1] in [' w ', ' — ']:
            text_window.SendKeys('{Left}', waitTime=0.07)
            text_window.SendKeys('{Shift}({Left 4})', waitTime=0.07)
            self.copy_button_control.Click(simulateMove=False)
            text_window.SendKeys('{Right}')
            test = pyperclip.paste()
            if test[0] == '€':
                text_window.SendKeys('{Left 3}{Back}{Right 4}')
            else:
                text_window.SendKeys('{Right}')
        if text_pos[-1] in (' ', '>', '('):
            text_window.SendKeys('€', waitTime=0)
            text_pos = self.abb_hdl.handle(text_window, text_pos)
            text_window.SendKeys('{Right}', waitTime=0)
            text_pos += 1
            while self.it_access.State == 0:
                time.sleep(0.001)
        return text_pos
