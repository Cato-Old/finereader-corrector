from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class DashHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count:pass_count + 3] in (' - ', '>- ', '>-\t'):
            new_dash = text[pass_count] + '— '
            text_window.SendKeys('{Shift}({Right 3})' + new_dash)
            text = text.replace(text[pass_count:pass_count + 3], new_dash, 1)
            pass_count += 3
        return text, pass_count
