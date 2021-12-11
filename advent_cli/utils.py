import argparse
import os
import re as re
import requests
import sys

from enum import Enum
from gettext import gettext
from importlib import import_module
from termcolor import colored as tc_colored

from . import config


class Status(Enum):
    PASS = 0
    FAIL = 1
    RATE_LIMIT = 2
    COMPLETED = 3
    UNKNOWN = 4


def colored(text, color):
    if config.get_config()['disable_color']:
        if text == '*':
            if color == 'cyan':
                return '/'
            elif color == 'grey':
                return '.'
        return text
    else:
        return tc_colored(text, color)


def compute_answers(year, day, solution_file='solution', example=False):
    sys.path.append(os.getcwd())
    solution = import_module(f'{year}.{day}.{solution_file}')
    with open(f'{year}/{day}/{"example_" if example else ""}input.txt', 'r') as f:
        data = solution.parse_input([
            line.replace('\r', '').replace('\n', '') for line in f.readlines()
        ])
    if not isinstance(data, tuple):
        data = (data,)
    part1_answer = solution.part1(*data)
    part2_answer = solution.part2(*data)
    return part1_answer, part2_answer


def submit_answer(year, day, level, answer):
    payload = {'level': level, 'answer': answer}
    r = requests.post(
        f'https://adventofcode.com/{year}/day/{int(day)}/answer',
        data=payload,
        cookies={'session': config.get_config()['session_cookie']}
    )
    response = r.text
    if "That's the right answer" in response:
        return Status.PASS, None
    elif "That's not the right answer" in response:
        return Status.FAIL, None
    elif 'You gave an answer too recently' in response:
        return Status.RATE_LIMIT, None
    elif 'Did you already complete it?' in response:
        return Status.COMPLETED, None
    else:
        return Status.UNKNOWN, response


# class to override default argparse formatter, because I don't think it looks very nice
# adapted from:
# https://github.com/python/cpython/blob/bffce2cbb5543bc63a67e33ad599328a12f2b00a/Lib/argparse.py#L154
class CustomHelpFormatter(argparse.RawTextHelpFormatter):

    class _Section(argparse.HelpFormatter._Section):
        # make section headings purple
        def __init__(self, formatter, parent, heading=None):
            if heading is not None:
                heading = colored(heading, 'magenta')
            super().__init__(formatter, parent, heading=heading)

    # add newlines to beginning and end
    def format_help(self):
        return f'\n{super().format_help()}\n'

    # make "usage:" purple
    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(
            usage, actions, groups,
            colored(gettext('usage: '), 'magenta') if prefix is None else prefix
        )

    # make arguments yellow
    def _format_action(self, action):
        return re.sub(r'(\-[a-zA-Z\-]+(\s)?([a-zA-Z_]+)?)', colored(r'\1', 'yellow'),
                      re.sub(r'(\s\s[a-zA-Z]+\s\s)', colored(r'\1', 'yellow'),
                             super()._format_action(action)))
