from uiautomation import PaneControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class ParagraphHandler(Handler):

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        if text_pos[-1] == '\n':
            if text_pos[0] not in ('$', '|'):
                text_window.SendKeys('$>', waitTime=0)
                text_pos.insert('$>')
                text_pos += 2
                if text_pos[0] in ('-', '—'):
                    text_window.SendKeys('{Shift}({Right 2})— {Left 2}',
                                         waitTime=0)
        return text_pos
