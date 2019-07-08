from uiautomation import PaneControl, ButtonControl

from app.cursor import TextPosition
from app.handlers.handler import Handler


class MiddleItalicHandler(Handler):

    def __init__(self, italic: ButtonControl) -> None:
        self.it_access = italic.GetLegacyIAccessiblePattern()
        self.it_invoke = italic.GetInvokePattern()

    def handle(self, text_window: PaneControl,
               text_pos: TextPosition) -> TextPosition:
        stop_chars = (' ', '(', '=', '>', '\t', '\n', '_', '[')
        while text_pos[-1] not in stop_chars or self.it_access.State != 0:
            if text_pos[-2:0] == '$>':
                text_window.SendKeys('{Shift}({Left 2})', waitTime=0)
                self.it_invoke.Invoke(waitTime=0)
                text_window.SendKeys('{Right}', waitTime=0)
                continue
            text_window.SendKeys('{Left}', waitTime=0)
            text_pos -= 1
        return text_pos
