import re
from time import sleep
from typing import Tuple, List

import pyperclip
from uiautomation import (ButtonControl, WindowControl, uiautomation,
                          PaneControl, ListControl)

from app.cursor import TextPosition
from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.begin_italic_handler import BeginItalicHandler
from app.handlers.code_handler import CodeHandler
from app.handlers.dash_handler import DashHandler
from app.handlers.end_italic_handler import EndItalicHandler
from app.handlers.end_quotation_mark_handler import EndQuotationMarkHandler
from app.handlers.handler import Handler
from app.handlers.internal_italic_handler import InternalItalicHandler
from app.handlers.middle_italic_handler import MiddleItalicHandler
from app.handlers.paragraph_handler import ParagraphHandler
from app.mappings import ANT, SUB, SUP


def handlers_initialize(
        italic: ButtonControl,
        copy_button_control: ButtonControl)-> Tuple[List[Handler],
                                                    List[Handler]]:
    normal_handlers = [AbbreviationHandler(italic),
                       EndQuotationMarkHandler(),
                       ParagraphHandler(),
                       DashHandler(),
                       ]
    italic_handlers = [MiddleItalicHandler(),
                       BeginItalicHandler(italic, copy_button_control),
                       InternalItalicHandler(italic),
                       EndItalicHandler(italic),
                       ]
    code_handler = [CodeHandler('|', ANT),
                    CodeHandler('|', SUP),
                    CodeHandler('▼', SUB),
                    ]
    normal_handlers += code_handler
    return normal_handlers, italic_handlers


def ui_automation_initialize()-> Tuple[WindowControl, ButtonControl,
                                       PaneControl, ButtonControl,
                                       ListControl]:
    fr_window = uiautomation.WindowControl(
        ClassName='FineReader12MainWindowClass')
    italic = uiautomation.ButtonControl(
        searchFromControl=fr_window, Name='Kursywa (Ctrl+I)')
    text_window = uiautomation.PaneControl(
        searchFromControl=fr_window, ClassName='$FineReaderEditorClass$')
    copy_button_control = uiautomation.ButtonControl(
        searchFromControl=fr_window, Name='Kopiuj (Ctrl+C)')
    page_list_control = uiautomation.ListControl(
        searchFromControl=fr_window, ClassName='SysListView32',
        AutomationId='3080')
    return (fr_window, italic, text_window, copy_button_control,
            page_list_control)


def text_position_initialise(
        text_window: PaneControl,
        copy_button_control: ButtonControl) -> TextPosition:
    text_window.SetFocus()
    sleep(0.5)
    text_window.SendKeys('{Ctrl}{Home}')
    sleep(0.5)
    text_window.SendKeys('{Shift}{Ctrl}{End}')
    copy_button_control.Click(simulateMove=False, waitTime=1)
    sleep(0.5)
    text_window.SendKeys('{Left}', waitTime=0)

    text = pyperclip.paste()
    text = re.sub('\r\n', '\n', text)
    text = re.sub('\n+', '\n', text)
    text = re.sub('—  ', '— ', text)

    return TextPosition(text, 0)
