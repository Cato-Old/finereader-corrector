from uiautomation import PaneControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class EndQuotationMarkHandler(Handler):

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[0:2] in ('" ', '".', '",'):
            text_window.SendKeys('{Shift}({Right})”', waitTime=0)
            text_pos.text = text_pos.text.replace(text_pos[0], '”', 1)
            text_pos += 1
        return text_pos


class BeginQuotationMarkHandler(Handler):

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[0:2] in (' "', '("', '>"'):
            text_window.SendKeys('{Right}{Shift}({Right})„', waitTime=0)
            text_pos.text = text_pos.text.replace(text_pos[1], '„', 1)
            text_pos += 2
        elif text_pos[-2:0] in (' "', '("', '>"'):
            text_window.SendKeys('{Shift}({Left})„', waitTime=0)
            text_pos.text = text_pos.text.replace(text_pos[-2], '„', 1)
        return text_pos
