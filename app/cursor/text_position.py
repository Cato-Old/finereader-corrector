from typing import Union, Optional

from uiautomation.uiautomation import PaneControl


class TextPosition:

    def __init__(
            self,
            text: str,
            pass_count: int,
            text_window: PaneControl = None
    ) -> None:
        self.text = text
        self.pos = pass_count
        self.text_window = text_window

    def __getitem__(self, ind: Union[slice, int]) -> Optional[str]:
        try:
            target_inds = (self.pos + ind.start, self.pos + ind.stop)
            if all(map(lambda x: x >= 0, target_inds)):
                return self.text[target_inds[0]:target_inds[1]]
            else:
                return None
        except AttributeError:
            target_ind = self.pos + ind
            if target_ind >= 0:
                return self.text[target_ind]
            else:
                return None

    def __iter__(self):
        args = (self.text, self.pos)
        return iter(args)

    def __add__(self, delta: int) -> 'TextPosition':
        self.pos = self.pos + delta
        return self

    def __iadd__(self, delta: int) -> 'TextPosition':
        self.pos = self.pos + delta
        return self

    def __sub__(self, delta: int) -> 'TextPosition':
        self.pos = self.pos - delta
        return self

    def __isub__(self, delta: int) -> 'TextPosition':
        self.pos = self.pos - delta
        return self

    def insert(self, ins: str) -> None:
        self.text = self.text[:self.pos] + ins + self.text[self.pos:]