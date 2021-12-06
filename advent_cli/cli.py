import argparse

from .commands import get

def main():
    parser = argparse.ArgumentParser()
    command_subparsers = parser.add_subparsers(dest='command', description='use advent {subcommand} --help for arguments')
    
    parser_get = command_subparsers.add_parser('get', help='download prompt and input, generate solution template')
    parser_get.add_argument('date', help='the year and day in YYYY/DD format (e.g. "2021/01")')
    
    args = parser.parse_args()
    
    if args.command == 'get':
        year, day = args.date.split('/')
        get(year, day)