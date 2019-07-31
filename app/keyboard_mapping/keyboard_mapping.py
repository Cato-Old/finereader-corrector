from functools import wraps
from time import sleep

import keyboard
from typing import Callable, List

MAPPING = {'exit_app': 'esc', 'pause_app': 'f11'}


class KeyboardMappings:
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

    @staticmethod
    @KeyMapping(mapping=MAPPING)
    def pause_app(key: str) -> None:
        if keyboard.is_pressed(key):
            while keyboard.is_pressed(key):
                sleep(0.01)
            while not keyboard.is_pressed(key):
                sleep(0.01)
            while keyboard.is_pressed(key):
                sleep(0.01)

    @staticmethod
    def get_all() -> List[Callable]:
        return [KeyboardMappings.exit_app, KeyboardMappings.pause_app]


