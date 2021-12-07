import os
import pytz
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime as dt
from markdownify import markdownify
from tabulate import tabulate

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

def stats(year):
    r = requests.get(f'https://adventofcode.com/{year}/leaderboard/self', cookies={'session': config.session_cookie})
    soup = BeautifulSoup(r.text, 'html.parser')
    
    table = soup.select('article pre')[0].text
    table_rows = [x.split() for x in table.split('\n')[2:-1]]
    
    stars_per_day = [0]*25
    for row in table_rows:
        stars_per_day[int(row[0])-1] = 2 if row[4:7] != ['-', '-', '-'] else 1 if row[1:4] != ['-', '-', '-'] else 0

    print('\n         1111111111222222\n1234567890123456789012345')
    
    for i, stars in enumerate(stars_per_day):
        today = dt.now(pytz.timezone('America/New_York'))
        if stars == 2:
            print(colored('*', 'yellow'), end='')
        elif stars == 1:
            print(colored('*', 'cyan'), end='')
        elif stars == 0 and today.year == int(year) and today.day < i+1:
            print(' ', end='')
        else:
            print(colored('*', 'grey'), end='')

    print(f" ({sum(stars_per_day)}{colored('*', 'yellow')})\n")
    print(f'({colored("*", "yellow")} 2 stars) ({colored("*", "cyan")} 1 star) ({colored("*", "grey")} 0 stars)\n')

    print(tabulate(table_rows, stralign='right', headers=['\nDay', 
        *['\n'.join([colored(y, 'cyan') for y in x.split('\n')]) for x in ['----\nTime', '(Part 1)\nRank', '----\nScore']],
        *['\n'.join([colored(y, 'yellow') for y in x.split('\n')]) for x in ['----\nTime', '(Part 2)\nRank', '----\nScore']]
    ]), '\n')