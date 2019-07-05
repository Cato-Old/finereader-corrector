class Cursor:

    def __init__(self, pass_count: int) -> None:
        self.pos = pass_count

    def slice(self, start: int, stop: int = None) -> slice:
        if stop:
            return slice(self.pos + start, self.pos + stop)
        else:
            return slice(self.pos + start, self.pos + start + 1)
