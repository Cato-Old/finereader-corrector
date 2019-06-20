from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class EndQuotationMarkHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if text[pass_count:pass_count + 2] in ('" ', '".', '",'):
            text_window.SendKeys('{Shift}({Right})', waitTime=0)
            text_window.SendKeys('”', waitTime=0)
            text = text.replace(text[pass_count:pass_count + 1], '”', 1)
            pass_count += 1
        return text, pass_count
