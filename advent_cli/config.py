import os
import sys

from .utils import colored

try:
    session_cookie = os.environ['ADVENT_SESSION_COOKIE']
except KeyError:
    print(colored('Session cookie not set.', 'red'))
    print(colored('Grab your AoC session cookie from a browser and store it in an environment variable ADVENT_SESSION_COOKIE.', 'red'))
    sys.exit(1)

try:
    private_leaderboards = os.environ['ADVENT_PRIV_BOARDS'].split(',')
except KeyError:
    private_leaderboards = []