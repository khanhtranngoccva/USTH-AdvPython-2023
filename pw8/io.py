import curses
import time
import typing

_terminal_ui = curses.initscr()
curses.endwin()


def terminal_print(message=None, clear=True):
    if message is None:
        message = ""
    if clear:
        _terminal_ui.clear()
        _terminal_ui.move(0, 0)
    y, x = _terminal_ui.getyx()
    _terminal_ui.refresh()
    _terminal_ui.addstr(y, 0, str(message))
    _terminal_ui.move(y + 1, 0)


def terminal_input(prompt="", clear=True):
    if clear:
        _terminal_ui.clear()
        _terminal_ui.addstr(0, 0, str(prompt))
    else:
        y, x = _terminal_ui.getyx()
        _terminal_ui.addstr(y, 0, str(prompt))

    curses.echo()
    user_input = _terminal_ui.getstr().decode("utf-8")
    curses.noecho()
    return user_input


def integer_input(prompt: typing.Union[str, None] = None, *args, **kwargs) -> int:
    while True:
        try:
            result = int(terminal_input(prompt, *args, **kwargs))
            break
        except ValueError:
            pass
    return result


def float_input(prompt: typing.Union[str, None] = None, *args, **kwargs) -> float:
    while True:
        try:
            result = float(terminal_input(prompt, *args, **kwargs))
            break
        except ValueError:
            pass
    return result


def terminal_start():
    global _terminal_ui
    _terminal_ui = curses.initscr()
    curses.noecho()
    curses.cbreak()
    _terminal_ui.keypad(True)


def terminal_shutdown():
    global _terminal_ui
    curses.echo()
    curses.nocbreak()
    _terminal_ui.keypad(False)
    curses.endwin()
