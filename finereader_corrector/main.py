import uiautomation
import keyboard
import pyperclip
import re
from time import sleep

SKR = {'A/^': 'Â', 'A/\'': 'Á', 'A/*': 'Å',
       'a/^': 'â', 'a/\'': 'á', 'a/*': 'å', 'a/`': 'à', 'a/:': 'ä', 'a/=': 'ā', 'a/(': 'ă',
       'E/\'': 'É', 'E/`': 'È',
       'e/<': 'ě', 'e/\'': 'é', 'e/`': 'è', 'e/:': 'ë', 'e/=': 'ē', 'e/^': 'ê', 'e/.': 'ė',
       'I/^': 'Î', 'I/\'': 'Í',
       'i/^': 'î', 'i/\'': 'í', 'i/:': 'ï', 'i/=': 'ī',
       'U/^': 'Û', 'U/\'': 'Ú', 'U/:': 'Ü',
       'u/^': 'û', 'u/\'': 'ú', 'u/:': 'ü', 'u/"': 'ű', 'u/`': 'ù', 'u/=': 'ū', 'u/,': 'ų',
       'O/:': 'Ö', 'O/|': 'Ø',
       'o/:': 'ö', 'o/~': 'õ', 'o/|': 'ø', 'o/"': 'ő', 'o/e': 'œ', 'o/,': 'ǫ', 'o/^': 'ô',
       'y/\'': 'ý', 'y/^': 'ŷ',
       'S/<': 'Š', 's/<': 'š', 'S/,': 'Ş', 's/,': 'ş', 's/.': 'ṣ', 'S/.': 'Ṣ',
       't/_': 'ṯ', 't/.': 'ṭ',
       'C/<': 'Č', 'c/<': 'č', 'c/,': 'ç',
       'r/<': 'ř',
       'n/<': 'ň', 'n/~': 'ñ',
       'z/<': 'ž',
       'g/.': 'ġ', 'G/<': 'Ǧ', 'G/(': 'Ğ', 'g/(': 'ğ',
       'h/.': 'ḥ', 'H/)': 'Ḫ', 'H/.': 'Ḥ', 'h/)': 'ḫ', 'h/_': 'ẖ',
       'D/-': 'Đ', 'd/-': 'đ', 'd/|': 'ð', 'd/.': 'ḍ',
       'A/E': 'Æ', 'a/e': 'æ',
       '|/>': 'Þ', '|/s': 'ß', '|/:': 'þ', '|/)': 'ь', ']/)': 'ъ'}
ANT = {'1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '0': '⁰'}
SUP = {'t': 'ᵗ', 'h': 'ʰ', 's': 'ˢ', 'r': 'ʳ', 'd': 'ᵈ', 'c': 'ᶜ', 'k': 'ᵏ', 'i': 'ⁱ', 'e': 'ᵉ', 'n': 'ⁿ'}
SUB = {'1': '₁', '2': '₂', '4': '₄', 'x': 'ₓ'}

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
    while pass_count < len(text):
        if keyboard.is_pressed('esc'):
            exit()
        if text[pass_count:pass_count + 3] in SKR.keys():
            TextWindow.SendKeys('{Shift}({Right 3})')
            TextWindow.SendKeys(SKR[text[pass_count:pass_count + 3]])
            text = text.replace(text[pass_count:pass_count + 3], SKR[text[pass_count:pass_count + 3]], 1)
            pass_count += 1
        elif text[pass_count:pass_count + 2] in ('" ', '".', '",'):
            TextWindow.SendKeys('{Shift}({Right})')
            TextWindow.SendKeys('”')
            text = text.replace(text[pass_count:pass_count + 1], '”', 1)
            pass_count += 1
        elif text[pass_count - 1:pass_count] == '\n':
            if text[pass_count:pass_count + 1] not in ('$', '|'):
                TextWindow.SendKeys('$>', waitTime=0)
                text = text.replace(text[pass_count - 1:pass_count], text[pass_count - 1:pass_count] + '$>', 1)
                pass_count += 2
                if text[pass_count:pass_count + 1] == '-':
                    TextWindow.SendKeys('{Shift}({Right 2})— {Left 2}')
                elif text[pass_count:pass_count + 2] == '—\t':
                    TextWindow.SendKeys('{Shift}({Right 2})— {Left 2}')
        elif text[pass_count:pass_count + 3] in (' - ', '>- ', '>-\t'):
            first_char = text[pass_count:pass_count + 1]
            TextWindow.SendKeys('{Shift}({Right 3})' +
                                first_char + '— ')
            text = text.replace(text[pass_count:pass_count + 3],
                                first_char + '— ', 1)
            pass_count += 3

        insCHR('|', ANT)
        insCHR('|', SUP)
        insCHR('▼', SUB)

        TextWindow.SendKeys('{Right}', waitTime=0, interval=0)
        pass_count += 1

        italic_pattern = Italic.GetLegacyIAccessiblePattern()
        if italic_pattern.State == 0:
            continue
        elif italic_pattern.State == 16:
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
            elif text[pass_count - 1] == ' ':
                TextWindow.SendKeys('€')
            elif pass_count > 1 and not text[pass_count - 2] in [' ', '(', '=', '>', '\t', '\n', '_', '[']:
                old_pass = pass_count
                while not text[pass_count - 2] in [' ', '_']:
                    TextWindow.SendKeys('{Left}')
                    pass_count -= 1
                TextWindow.SendKeys('{Left}€')
                pass_count -= 1
#                if italic_pattern.State == 0:
#                    n = old_pass - pass_count
#                    TextWindow.SendKeys('{Shift}({Right ' + str(n) + '})')
#                    Italic.GetInvokePattern().Invoke()
#                    TextWindow.SendKeys('{Right}')
#                    pass_count += n
#                else:
                TextWindow.SendKeys('{Right}')
                pass_count += 1
            else:
                TextWindow.SendKeys('{Left}€{Right}')
            it_str = text[pass_count - 1:pass_count + 1]
            while italic_pattern.State == 16:
                if text[pass_count:pass_count + 3] in SKR.keys():
                    TextWindow.SendKeys('{Shift}({Right 3})')
                    TextWindow.SendKeys(SKR[text[pass_count:pass_count + 3]])
                    text = text.replace(text[pass_count:pass_count + 3], SKR[text[pass_count:pass_count + 3]], 1)
                    pass_count += 1
                    continue

                insCHR('|', SUP)

                TextWindow.SendKeys('{Right}', waitTime=0)
                pass_count += 1

                if pass_count >= len(text):
                    Italic.GetInvokePattern().Invoke()
                    TextWindow.SendKeys('€')
                    break
                it_str += text[pass_count]
            if it_str:
                it_str = it_str[:-2]
            else:
                continue
            print(it_str)
            if it_str[-1] in [',', '.', ' ', ';']:
                if it_str[-3:] in [' r.', ' w.', '...'] or it_str[-4:] == ' al.' or it_str[-5:] == ' cit.':
                    TextWindow.SendKeys('{Left}€{Right}', waitTime=0.01)
                else:
                    TextWindow.SendKeys('{Left 2}')
                    Italic.GetInvokePattern().Invoke()
                    TextWindow.SendKeys('€{Right 2}')
            elif it_str[-2:] == ', ':
                print(it_str)
                TextWindow.SendKeys('{Left 3}€{Right 3}', waitTime=0.01)
            else:
                TextWindow.SendKeys('{Left}', waitTime=0.01)
                Italic.GetInvokePattern().Invoke()
                TextWindow.SendKeys('€', waitTime=0.01)
                pass_count -= 1
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
