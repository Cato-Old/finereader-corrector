from typing import Tuple, List

from uiautomation import ButtonControl

from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.begin_italic_handler import BeginItalicHandler
from app.handlers.dash_handler import DashHandler
from app.handlers.end_italic_handler import EndItalicHandler
from app.handlers.end_quotation_mark_handler import EndQuotationMarkHandler
from app.handlers.handler import Handler
from app.handlers.internal_italic_handler import InternalItalicHandler
from app.handlers.middle_italic_handler import MiddleItalicHandler
from app.handlers.paragraph_handler import ParagraphHandler


def handlers_initialize(italic: ButtonControl)-> Tuple[List[Handler],
                                                       List[Handler]]:
    normal_handlers = [AbbreviationHandler(italic),
                       EndQuotationMarkHandler(),
                       ParagraphHandler(),
                       DashHandler(),
                       ]
    italic_handlers = [MiddleItalicHandler(),
                       BeginItalicHandler(italic),
                       InternalItalicHandler(italic),
                       EndItalicHandler(italic),
                       ]
    return normal_handlers, italic_handlers
