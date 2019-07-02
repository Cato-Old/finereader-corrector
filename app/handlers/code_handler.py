from typing import Tuple

from uiautomation import PaneControl

from app.handlers.handler import Handler


class CodeHandler(Handler):

    def __init__(self, precode: str, dictionary: dict) -> None:
        self.precode = precode
        self.dict = dictionary

    def handle(self, text_window: PaneControl,
               text: str, pass_count: int) -> Tuple[str, int]:
        keys = [self.precode + key for key in self.dict.keys()]
        if text[pass_count:pass_count + 2] in keys:
            n = -1
            while True:
                n += 1
                code = slice(pass_count + 1 + n,
                             pass_count + 2 + n)
                if text[code] not in self.dict.keys():
                    n -= 1
                    break
            text_window.SendKeys('{Shift}({Right ' + str(2 + n) + '})',
                                 waitTime=0)
            chars_new = ''
            for char in text[pass_count + 1:pass_count + 2 + n]:
                chars_new += self.dict[char]
            text_window.SendKeys(chars_new, waitTime=0)
            text = text.replace(text[pass_count:pass_count + 2 + n],
                                chars_new, 1)
            pass_count += 1 + n
        return text, pass_count
