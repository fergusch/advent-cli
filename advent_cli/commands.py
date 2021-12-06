import os
import re
import requests

from bs4 import BeautifulSoup
from markdownify import markdownify

from . import config
from .utils import colored

def get(year, day):
    try:
        os.makedirs(f'{year}/{day}')
    except FileExistsError:
        print(colored(f'Folder {year}/{day} already exists.', 'red'))
        return

    r = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}', cookies={'session': config.session_cookie})
    soup = BeautifulSoup(r.text, 'html.parser')
    part1_html = soup.find('article', class_='day-desc').decode_contents()

    # remove hyphens from title sections, makes markdown look nicer
    part1_html = re.sub('--- (.*) ---', r'\1', part1_html)

    # also makes markdown look better
    part1_html = part1_html.replace('\n\n', '\n')

    with open(f'{year}/{day}/prompt.md', 'w') as f:
        f.write(markdownify(part1_html))
    print(f'Downloaded prompt to {year}/{day}/prompt.md')

    r = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}/input', cookies={'session': config.session_cookie})
    with open(f'{year}/{day}/input.txt', 'w') as f:
        f.write(r.text)
    print(f'Downloaded input to {year}/{day}/input.txt')

    with open(f'{year}/{day}/example_input.txt', 'w') as f:
        f.write('\n')
    print(f'Created {year}/{day}/example_input.txt')

    with open(f'{year}/{day}/solution.py', 'w') as f:
            f.write(f'## advent of code {year}\n## https://adventofcode.com/{year}\n## day {day}\n\n' + \
                    'def parse_input(lines):\n    pass\n\n' + \
                    'def part1(data):\n    pass\n\n' + \
                    'def part2(data):\n    pass')
    print(f'Created {year}/{day}/solution.py')