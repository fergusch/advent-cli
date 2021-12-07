import os
import requests
import sys

from enum import Enum
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
    if config.disable_color:
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
        data = solution.parse_input([line.strip() for line in f.readlines()])
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
        cookies={'session': config.session_cookie}
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
