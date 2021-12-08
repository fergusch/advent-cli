import os
import pytz
import re
import requests

from bs4 import BeautifulSoup
from datetime import datetime as dt
from markdownify import markdownify
from tabulate import tabulate

from . import config
from .utils import colored, compute_answers, submit_answer, Status


def get(year, day):
    if os.path.exists(f'{year}/{day}/'):
        print(colored('Directory already exists:', 'red'))
        print(colored(f'  {os.getcwd()}/{year}/{day}/', 'red'))
        return

    r = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}',
                     cookies={'session': config.session_cookie})
    if r.status_code == 404:
        if 'before it unlocks!' in r.text:
            print(colored('This puzzle has not unlocked yet.', 'red'))
            print(colored(f'It will unlock on Dec {day} {year} at midnight EST (UTC-5).',
                          'red'))
            return
        else:
            print(colored('The server returned error 404 for url:', 'red'))
            print(colored(f'  "https://adventofcode.com/{year}/day/{int(day)}/"', 'red'))
            return

    soup = BeautifulSoup(r.text, 'html.parser')
    part1_html = soup.find('article', class_='day-desc').decode_contents()

    # remove hyphens from title sections, makes markdown look nicer
    part1_html = re.sub('--- (.*) ---', r'\1', part1_html)

    # also makes markdown look better
    part1_html = part1_html.replace('\n\n', '\n')

    with open(f'{year}/{day}/prompt.md', 'w') as f:
        f.write(markdownify(part1_html))
    print(f'Downloaded prompt to {year}/{day}/prompt.md')

    r = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}/input',
                     cookies={'session': config.session_cookie})
    with open(f'{year}/{day}/input.txt', 'w') as f:
        f.write(r.text)
    print(f'Downloaded input to {year}/{day}/input.txt')

    open(f'{year}/{day}/example_input.txt', 'w').close()
    print(f'Created {year}/{day}/example_input.txt')

    with open(f'{year}/{day}/solution.py', 'w') as f:
        f.write(f'## advent of code {year}\n'
                f'## https://adventofcode.com/{year}\n'
                f'## day {day}\n\n'
                'def parse_input(lines):\n    pass\n\n'
                'def part1(data):\n    pass\n\n'
                'def part2(data):\n    pass')
    print(f'Created {year}/{day}/solution.py')


def stats(year):
    r = requests.get(f'https://adventofcode.com/{year}/leaderboard/self',
                     cookies={'session': config.session_cookie})
    soup = BeautifulSoup(r.text, 'html.parser')

    table = soup.select('article pre')[0].text
    table_rows = [x.split() for x in table.split('\n')[2:-1]]

    stars_per_day = [0] * 25
    for row in table_rows:
        stars_per_day[int(row[0]) - 1] = 2 if row[4:7] != ['-', '-', '-'] \
                                           else 1 if row[1:4] != ['-', '-', '-'] \
                                           else 0

    print('\n         1111111111222222\n1234567890123456789012345')

    for i, stars in enumerate(stars_per_day):
        today = dt.now(pytz.timezone('America/New_York'))
        if stars == 2:
            print(colored('*', 'yellow'), end='')
        elif stars == 1:
            print(colored('*', 'cyan'), end='')
        elif stars == 0 and today.year == int(year) and today.day < (i + 1):
            print(' ', end='')
        else:
            print(colored('*', 'grey'), end='')

    print(f" ({sum(stars_per_day)}{colored('*', 'yellow')})\n")
    print(f'({colored("*", "yellow")} 2 stars) '
          f'({colored("*", "cyan")} 1 star) '
          f'({colored("*", "grey")} 0 stars)\n')

    print(tabulate(table_rows, stralign='right', headers=[
        '\nDay',
        *['\n'.join([colored(y, 'cyan') for y in x.split('\n')])
            for x in ['----\nTime', '(Part 1)\nRank', '----\nScore']],
        *['\n'.join([colored(y, 'yellow') for y in x.split('\n')])
            for x in ['----\nTime', '(Part 2)\nRank', '----\nScore']]
    ]), '\n')

    if config.private_leaderboards:
        print(colored(f'You are a member of {len(config.private_leaderboards)} '
                      f'private leaderboard(s).', 'grey'))
        print(colored(f'Use "advent stats {year} --private" to see them.\n', 'grey'))


def private_leaderboard_stats(year):
    if config.private_leaderboards:
        for board_id in config.private_leaderboards:
            r = requests.get(
                f'https://adventofcode.com/{year}/leaderboard/private/view/{board_id}',
                cookies={'session': config.session_cookie}
            )
            soup = BeautifulSoup(r.text, 'html.parser')

            board_owner = re.findall(r'private leaderboard of (.*) for',
                                     soup.select('article p')[0].text)[0]
            rows = soup.find_all('div', class_='privboard-row')[1:]

            top_score_len = len(rows[0].find_all(text=True, recursive=False)[0].strip())
            print(f"\n{board_owner}'s private leaderboard {colored(f'({board_id})', 'grey')}")
            print(f'\n{" "*(top_score_len+14)}1111111111222222'
                  f'\n{" "*(top_score_len+5)}1234567890123456789012345')

            for row in rows:
                position = row.find('span', class_='privboard-position').text
                stars = row.find_all('span', class_=re.compile('privboard-star-*'))
                name = row.find('span', class_='privboard-name').text
                name_link = row.select('.privboard-name a')[0].attrs['href'] \
                    if len(row.select('.privboard-name a')) else None
                score = row.find_all(text=True, recursive=False)[0].strip()

                print(f'{position} {score:>{top_score_len}}', end=' ')
                for span in stars:
                    class_ = span.attrs['class'][0]
                    if 'both' in class_:
                        print(colored('*', 'yellow'), end='')
                    elif 'firstonly' in class_:
                        print(colored('*', 'cyan'), end='')
                    elif 'unlocked' in class_:
                        print(colored('*', 'grey'), end='')
                    elif 'locked' in class_:
                        print(' ', end='')

                print(f' {name}', end=' ')
                print(f'({colored(name_link, "blue")})' if name_link is not None else '')

            print()
            print(f'({colored("*", "yellow")} 2 stars) '
                  f'({colored("*", "cyan")} 1 star) '
                  f'({colored("*", "grey")} 0 stars)\n')
    else:
        print(colored('You are not a member of any private leaderboards '
                      'or you have not configured them.', 'red'))
        print(colored('Set the environment variable ADVENT_PRIV_BOARDS to '
                      'a comma-separated list of private leaderboard IDs.', 'red'))


def test(year, day, solution_file='solution', example=False):

    if not os.path.exists(f'{year}/{day}/'):
        print(colored('Directory does not exist:', 'red'))
        print(colored(f'  "{os.getcwd()}/{year}/{day}/"', 'red'))
        return

    if example:
        if os.stat(f'{year}/{day}/example_input.txt').st_size == 0:
            print(colored('Example input file is empty:', 'red'))
            print(colored(f'  {os.getcwd()}/{year}/{day}/example_input.txt', 'red'))
            return
        else:
            print(colored('(Using example input)', 'red'))

    if solution_file != 'solution':
        if not os.path.exists(f'{year}/{day}/{solution_file}.py'):
            print(colored('Solution file does not exist:', 'red'))
            print(colored(f'  "{os.getcwd()}/{year}/{day}/{solution_file}.py"', 'red'))
            return
        print(colored(f'(Using {solution_file}.py)', 'red'))

    part1_answer, part2_answer = compute_answers(year, day,
                                                 solution_file=solution_file,
                                                 example=example)
    if part1_answer is not None:
        print(f'{colored("Part 1:", "cyan")} {part1_answer}')
        if part2_answer is not None:
            print(f'{colored("Part 2:", "yellow")} {part2_answer}')
    else:
        print(colored('No solution implemented', 'red'))
        return

    if solution_file != 'solution':
        part1_answer_orig, part2_answer_orig = compute_answers(year, day, example=example)
        if part1_answer == part1_answer_orig and part2_answer == part2_answer_orig:
            print(colored('Output matches solution.py', 'green'))
        else:
            print(colored('Output does not match solution.py', 'red'))


def submit(year, day, solution_file='solution'):

    if not os.path.exists(f'{year}/{day}/'):
        print(colored('Directory does not exist:', 'red'))
        print(colored(f'  "{os.getcwd()}/{year}/{day}/"', 'red'))
        return

    if solution_file != 'solution':
        if not os.path.exists(f'{year}/{day}/{solution_file}.py'):
            print(colored('Solution file does not exist:', 'red'))
            print(colored(f'  "{os.getcwd()}/{year}/{day}/{solution_file}.py"', 'red'))
            return
        print(colored(f'(Using {solution_file}.py)', 'red'))

    part1_answer, part2_answer = compute_answers(year, day, solution_file=solution_file)

    status, response = None, None
    if part2_answer is not None:
        print('Submitting part 2...')
        status, response = submit_answer(year, day, 2, part2_answer)
    elif part1_answer is not None:
        print('Submitting part 1...')
        status, response = submit_answer(year, day, 1, part1_answer)
    else:
        print(colored('No solution implemented', 'red'))
        return

    if status == Status.PASS:
        print(colored('Correct!', 'green'), end=' ')
        if part2_answer is not None:
            print(colored('**', 'yellow'))
            print(f'Day {int(day)} complete!')
        elif part1_answer is not None:
            print(colored('*', 'cyan'))
            r = requests.get(f'https://adventofcode.com/{year}/day/{int(day)}',
                             cookies={'session': config.session_cookie})
            soup = BeautifulSoup(r.text, 'html.parser')
            part2_html = soup.find_all('article', class_='day-desc')[1].decode_contents()

            # remove hyphens from title sections, makes markdown look nicer
            part2_html = re.sub('--- (.*) ---', r'\1', part2_html)

            # also makes markdown look better
            part2_html = part2_html.replace('\n\n', '\n')

            with open(f'{year}/{day}/prompt.md', 'a') as f:
                f.write(markdownify(part2_html))
            print(f'Appended part 2 prompt to {year}/{day}/prompt.md')

    elif status == Status.FAIL:
        print(colored('Incorrect!', 'red'))

    elif status == Status.RATE_LIMIT:
        print(colored('Rate limited! Please wait before submitting again.', 'yellow'))

    elif status == Status.COMPLETED:
        print(colored("You've already completed this question.", 'yellow'))

    elif status == Status.UNKNOWN:
        print(colored('Something went wrong. Please view the output below:', 'red'))
        print(response)
