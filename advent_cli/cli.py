import argparse

from . import config
from .commands import get, stats, private_leaderboard_stats, test
from ._version import __version__

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('--disable-color', dest='disable_color', action='store_true', 
        help='disable coloring terminal output' + \
            '\n(set env. variable ADVENT_DISABLE_TERMCOLOR=1 to disable permanently)',
    )

    command_subparsers = parser.add_subparsers(dest='command', description='use advent {subcommand} --help for arguments')
    
    parser_get = command_subparsers.add_parser('get', help='download prompt and input, generate solution template')
    parser_get.add_argument('date', help='the year and day in YYYY/DD format (e.g. "2021/01")')
    
    parser_stats = command_subparsers.add_parser('stats', help='show personal stats or private leaderboards')
    parser_stats.add_argument('year', help='year to show stats for')
    parser_stats.add_argument('-p', '--private', dest='show_private', action='store_true', help='show private leaderboard(s)')

    parser_test = command_subparsers.add_parser('test', help='run solution and output answers without submitting')
    parser_test.add_argument('date', help='the year and day in YYYY/DD format (e.g. "2021/01")')

    args = parser.parse_args()

    if args.disable_color:
        config.disable_color = True
    
    if args.command == 'get':
        year, day = args.date.split('/')
        get(year, day)

    elif args.command == 'stats':
        if args.show_private:
            private_leaderboard_stats(args.year)
        else:
            stats(args.year)

    elif args.command == 'test':
        year, day = args.date.split('/')
        test(year, day)