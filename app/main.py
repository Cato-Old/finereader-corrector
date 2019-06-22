import time

import uiautomation
import keyboard
import pyperclip
import re
from time import sleep

from app.handlers.abbreviation_handler import AbbreviationHandler
from app.handlers.begin_italic_handler import BeginItalicHandler
from app.handlers.dash_handler import DashHandler
from app.handlers.end_quotation_mark_handler import EndQuotationMarkHandler
from app.handlers.internal_italic_handler import InternalItalicHandler
from app.handlers.middle_italic_handler import MiddleItalicHandler
from app.handlers.paragraph_handler import ParagraphHandler
from app.mappings import SKR, ANT, SUB, SUP

FRWindow = uiautomation.WindowControl(ClassName='FineReader12MainWindowClass')

Italic = uiautomation.ButtonControl(searchFromControl=FRWindow, Name='Kursywa (Ctrl+I)')
TextWindow = uiautomation.PaneControl(searchFromControl=FRWindow, ClassName='$FineReaderEditorClass$')
CopyButtonControl = uiautomation.ButtonControl(searchFromControl=FRWindow, Name='Kopiuj (Ctrl+C)')
PageListControl = uiautomation.ListControl(searchFromControl=FRWindow, ClassName='SysListView32', AutomationId='3080')


def insCHR(precode, Dict):
    global text, pass_count

    if text[pass_count:pass_count + 2] in [precode + key for key in Dict.keys()]:
        n = -1
        while True:
            n += 1
            if text[pass_count + 1 + n:pass_count + 2 + n] not in Dict.keys():
                n -= 1
                break
        TextWindow.SendKeys('{Shift}({Right ' + str(2 + n) + '})')
        chars_new = ''
        for char in text[pass_count + 1:pass_count + 2 + n]:
            chars_new += Dict[char]
        TextWindow.SendKeys(chars_new)
        text = text.replace(text[pass_count:pass_count + 2 + n], chars_new, 1)
        pass_count += 1 + n


def corrector():
    global text, pass_count

    TextWindow.SetFocus()
    sleep(1)
    TextWindow.SendKeys('{Ctrl}{Home}')
    sleep(1)
    TextWindow.SendKeys('{Shift}{Ctrl}{End}')
    CopyButtonControl.Click(simulateMove=False, waitTime=1)
    sleep(1)
    TextWindow.SendKeys('{Left}')

    text = pyperclip.paste()
    text = re.sub('\r\n', '\n', text)
    text = re.sub('\n+', '\n', text)
    text = re.sub('—  ', '— ', text)

    pass_count = 0
    normal_handlers = [
        AbbreviationHandler(Italic),
        EndQuotationMarkHandler(),
        ParagraphHandler(),
        DashHandler(),
    ]
    while pass_count < len(text):
        if keyboard.is_pressed('esc'):
            exit()
        for hdl in normal_handlers:
            text, pass_count = hdl.handle(TextWindow, text, pass_count)

        insCHR('|', ANT)
        insCHR('|', SUP)
        insCHR('▼', SUB)

        TextWindow.SendKeys('{Right}', waitTime=0, interval=0)
        pass_count += 1

        italic_pattern = Italic.GetLegacyIAccessiblePattern()

        if italic_pattern.State == 0:
            continue
        elif italic_pattern.State == 16:
            italic_handlers = [
                MiddleItalicHandler(),
                BeginItalicHandler(Italic),
                InternalItalicHandler(Italic),
            ]
            print('Pierwsze znaki italicu: ' + text[pass_count - 1:pass_count + 1])
            if text[pass_count - 4:pass_count - 1] in [' w ', ' — '] and pass_count > 3:
                TextWindow.SendKeys('{Left}', waitTime=0.07)
                TextWindow.SendKeys('{Shift}({Left 4})', waitTime=0.07)
                CopyButtonControl.Click(simulateMove=False)
                TextWindow.SendKeys('{Right}')
                test = pyperclip.paste()
                print(test)
                if test[0] == '€':
                    TextWindow.SendKeys('{Left 3}{Back}{Right 4}')
                else:
                    TextWindow.SendKeys('€{Right}')
            elif text[pass_count - 1:pass_count + 1] == ', ':
                TextWindow.SendKeys('{Right}')
                pass_count += 1
                if italic_pattern.State == 16:
                    TextWindow.SendKeys('€')
            for hdl in italic_handlers:
                text, pass_count = hdl.handle(TextWindow, text, pass_count)
#                if italic_pattern.State == 0:
#                    n = old_pass - pass_count
#                    TextWindow.SendKeys('{Shift}({Right ' + str(n) + '})')
#                    Italic.GetInvokePattern().Invoke()
#                    TextWindow.SendKeys('{Right}')
#                    pass_count += n
#                else:
#                TextWindow.SendKeys('{Right}')
#                pass_count += 1
#            else:
#                TextWindow.SendKeys('{Left}€{Right}')
#            it_str = text[pass_count - 1:pass_count + 1]
#
#            if it_str:
#                it_str = it_str[:-2]
#            else:
#                continue
#            print(it_str)
#            if it_str[-1] in [',', '.', ' ', ';']:
#                if it_str[-3:] in [' r.', ' w.', '...'] or it_str[-4:] == ' al.' or it_str[-5:] == ' cit.':
#                    TextWindow.SendKeys('{Left}€{Right}', waitTime=0.01)
#                else:
#                    TextWindow.SendKeys('{Left 2}')
#                    Italic.GetInvokePattern().Invoke()
#                    TextWindow.SendKeys('€{Right 2}')
#            elif it_str[-2:] == ', ':
#                print(it_str)
#                TextWindow.SendKeys('{Left 3}€{Right 3}', waitTime=0.01)
#            else:
            TextWindow.SendKeys('{Left}', waitTime=0)
            TextWindow.SendKeys('€{Right}', waitTime=0)
            while italic_pattern.State == 16:
                time.sleep(0.001)
    return text


FRWindow.SetActive()
Pages = PageListControl.GetChildren()
if Pages[0].ControlTypeName == 'ScrollBarControl':
    PagesScrollBar = Pages[0]
    Pages = Pages[1:]
for page in Pages:
    if keyboard.is_pressed('esc'):
        exit()
    if page.IsOffscreen:
        PagesScrollBar.WheelDown()
    page.Click()
    t = corrector()
