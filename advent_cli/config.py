import os
import sys
from termcolor import colored


def get_config():

    config = {}

    if 'ADVENT_PRIV_BOARDS' in os.environ:
        config['private_leaderboards'] = os.environ['ADVENT_PRIV_BOARDS'].split(',')
    else:
        config['private_leaderboards'] = []

    if 'ADVENT_DISABLE_TERMCOLOR' in os.environ:
        config['disable_color'] = (os.environ['ADVENT_DISABLE_TERMCOLOR'] == '1')
    else:
        config['disable_color'] = False

    if 'ADVENT_SESSION_COOKIE' in os.environ:
        config['session_cookie'] = os.environ['ADVENT_SESSION_COOKIE']
    else:
        # this is to avoid importing colored() from utils.py, resulting in a circular import
        error_message = ('Session cookie not set.\nGrab your AoC session cookie from a browser'
                         ' and store it in an environment variable ADVENT_SESSION_COOKIE.')
        if not config['disable_color']:
            error_message = '\n'.join([colored(s, 'red') for s in error_message.split('\n')])
        print(error_message)
        sys.exit(1)

    return config
