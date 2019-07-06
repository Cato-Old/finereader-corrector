from typing import Union


class TextPosition:

    def __init__(self, text: str, pass_count: int) -> None:
        self.text = text
        self.pos = pass_count

    def __getitem__(self, ind: Union[slice, int]) -> str:
        try:
            return self.text[self.pos + ind.start :
                             self.pos + ind.stop]
        except AttributeError:
            return self.text[self.pos + ind]
