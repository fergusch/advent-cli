import os
import sys

from .utils import colored

if 'ADVENT_SESSION_COOKIE' in os.environ:
    session_cookie = os.environ['ADVENT_SESSION_COOKIE']
else:
    print(colored('Session cookie not set.', 'red'))
    print(colored('Grab your AoC session cookie from a browser and store it in an environment variable ADVENT_SESSION_COOKIE.', 'red'))
    sys.exit(1)

if 'ADVENT_PRIV_BOARDS' in os.environ:
    private_leaderboards = os.environ['ADVENT_PRIV_BOARDS'].split(',')
else:
    private_leaderboards = []