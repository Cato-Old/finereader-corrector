from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class ParagraphHandler(Handler):

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        if pass_count > 0 and text[pass_count - 1] == '\n':
            if text[pass_count] not in ('$', '|'):
                text_window.SendKeys('$>', waitTime=0)
                text = text.replace(text[pass_count - 1],
                                    text[pass_count - 1] + '$>', 1)
                pass_count += 2
                if text[pass_count] in ('-', '—'):
                    text_window.SendKeys('{Shift}({Right 2})— {Left 2}',
                                         waitTime=0)
        return text, pass_count
