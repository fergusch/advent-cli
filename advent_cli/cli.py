import argparse

from .commands import get, stats, private_leaderboard_stats

def main():
    parser = argparse.ArgumentParser()
    command_subparsers = parser.add_subparsers(dest='command', description='use advent {subcommand} --help for arguments')
    
    parser_get = command_subparsers.add_parser('get', help='download prompt and input, generate solution template')
    parser_get.add_argument('date', help='the year and day in YYYY/DD format (e.g. "2021/01")')
    
    parser_stats = command_subparsers.add_parser('stats', help='show personal stats or private leaderboards')
    parser_stats.add_argument('year', help='year to show stats for')
    parser_stats.add_argument('-p', '--private', dest='show_private', action='store_true', help='show private leaderboard(s)')

    args = parser.parse_args()
    
    if args.command == 'get':
        year, day = args.date.split('/')
        get(year, day)

    elif args.command == 'stats':
        if args.show_private:
            private_leaderboard_stats(args.year)
        else:
            stats(args.year)