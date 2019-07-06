import uiautomation
import keyboard
import pyperclip
import re
from time import sleep

from app.initializing import handlers_initialize, text_position_initialise
from app.initializing import ui_automation_initialize


def corrector(italic: uiautomation.ButtonControl,
              text_window: uiautomation.PaneControl,
              copy_button_control: uiautomation.ButtonControl) -> str:
    global text, pass_count
    normal_handlers, italic_handlers = handlers_initialize(italic)
    text, pass_count = text_position_initialise(text_window,
                                                copy_button_control)

    while pass_count < len(text):
        if keyboard.is_pressed('esc'):
            exit()
        for hdl in normal_handlers:
            text, pass_count = hdl.handle(text_window, text, pass_count)

        text_window.SendKeys('{Right}', waitTime=0, interval=0)
        pass_count += 1

        italic_pattern = italic.GetLegacyIAccessiblePattern()

        if italic_pattern.State == 0:
            continue
        elif italic_pattern.State == 16:
            print('Pierwsze znaki italicu: ' + text[pass_count - 1:pass_count + 1])
            if text[pass_count - 4:pass_count - 1] in [' w ', ' — '] and pass_count > 3:
                text_window.SendKeys('{Left}', waitTime=0.07)
                text_window.SendKeys('{Shift}({Left 4})', waitTime=0.07)
                copy_button_control.Click(simulateMove=False)
                text_window.SendKeys('{Right}')
                test = pyperclip.paste()
                print(test)
                if test[0] == '€':
                    text_window.SendKeys('{Left 3}{Back}{Right 4}')
                else:
                    text_window.SendKeys('€{Right}')
            elif text[pass_count - 1:pass_count + 1] == ', ':
                text_window.SendKeys('{Right}')
                pass_count += 1
                if italic_pattern.State == 16:
                    text_window.SendKeys('€')
            for hdl in italic_handlers:
                text, pass_count = hdl.handle(text_window, text, pass_count)
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
    return text


def main(fr_window: uiautomation.WindowControl,
         italic: uiautomation.ButtonControl,
         text_window: uiautomation.PaneControl,
         copy_button_control: uiautomation.ButtonControl,
         page_list_control: uiautomation.ListControl
         ) -> None:
    fr_window.SetActive()
    pages = page_list_control.GetChildren()
    if pages[0].ControlTypeName == 'ScrollBarControl':
        pages_scroll_bar = pages[0]
        pages = pages[1:]
    for page in pages:
        if keyboard.is_pressed('esc'):
            exit()
        if page.IsOffscreen:
            pages_scroll_bar.WheelDown()
        page.Click()
        t = corrector(italic, text_window, copy_button_control)


main(*ui_automation_initialize())
