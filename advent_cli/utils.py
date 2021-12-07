import os
import sys

from importlib import import_module
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