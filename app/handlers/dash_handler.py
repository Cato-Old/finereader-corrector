from typing import Tuple

from uiautomation import PaneControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class DashHandler(Handler):

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[0:3] in (' - ', '>- ', '>-\t'):
            new_dash = text_pos[0] + '— '
            text_window.SendKeys('{Shift}({Right 3})' + new_dash, waitTime=0)
            text_pos.text = text_pos.text.replace(text_pos[0:3], new_dash, 1)
            text_pos += 3
        return text_pos
