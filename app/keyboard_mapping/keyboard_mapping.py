from functools import wraps

import keyboard
from typing import Callable

MAPPING = {'exit_app': 'esc', 'pause_app': 'f11'}


class KeyboardMapping:
    class KeyMapping:

        def __init__(self, mapping: dict = None) -> None:
            self.mapping = mapping

        def __call__(self, func: Callable) -> Callable:
            name = func.__name__

            @wraps(func)
            def wrapper() -> None:
                func(self.mapping[name])

            return wrapper

    @staticmethod
    @KeyMapping(mapping=MAPPING)
    def exit_app(key: str) -> None:
        if keyboard.is_pressed(key):
            exit()
