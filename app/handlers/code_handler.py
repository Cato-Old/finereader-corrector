from uiautomation import PaneControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class CodeHandler(Handler):

    def __init__(self, precode: str, dictionary: dict) -> None:
        self.precode = precode
        self.dict = dictionary

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        keys = [self.precode + key for key in self.dict.keys()]
        if text_pos[0:2] in keys:
            n = self.__count_chars(text_pos)
            text_window.SendKeys('{Shift}({Right ' + str(1 + n) + '})',
                                 waitTime=0)
            chars_new = ''
            for char in text_pos[1:1 + n]:
                chars_new += self.dict[char]
            text_window.SendKeys(chars_new + '{Left}', waitTime=0)
            text_pos.text = text_pos.text.replace(text_pos[0:1 + n],
                                                  chars_new, 1)
            text_pos += n - 1
        return text_pos

    def __count_chars(self, text_pos: TextPosition) -> int:
        n = 0
        while True:
            if text_pos[n + 1: n + 2] not in self.dict.keys():
                break
            else:
                n += 1
        return n
