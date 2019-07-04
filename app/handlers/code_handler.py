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
            n = self.__count_chars(text, pass_count)
            text_window.SendKeys('{Shift}({Right ' + str(1 + n) + '})',
                                 waitTime=0)
            chars_new = ''
            for char in text[pass_count + 1:pass_count + 1 + n]:
                chars_new += self.dict[char]
            text_window.SendKeys(chars_new + '{Left}', waitTime=0)
            text = text.replace(text[pass_count:pass_count + 1 + n],
                                chars_new, 1)
            pass_count += n-1
        return text, pass_count

    def __count_chars(self, text: str, pass_count: int) -> int:
        n = 0
        while True:
            char = slice(pass_count + 1 + n,
                         pass_count + 2 + n)
            if text[char] not in self.dict.keys():
                break
            else:
                n += 1
        return n
