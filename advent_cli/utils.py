from termcolor import colored as tc_colored

from . import config

def colored(text, color):
    if config.disable_color:
        if text == '*':
            if color == 'cyan':
                return '/'
            elif color == 'grey':
                return '.'
        return text
    else:
        return tc_colored(text, color)