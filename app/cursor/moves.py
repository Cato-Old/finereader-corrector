from app.cursor import TextPosition


def forward(text_pos: TextPosition, count: int) -> TextPosition:
    text_control = text_pos.text_window
    try:
        text_control.SendKeys(f'{{Right {count}}}', waitTime=0, interval=0)
        text_pos += count
    except AttributeError as err:
        print(err)
    return text_pos

