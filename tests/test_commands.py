from mock import patch, call, mock_open, MagicMock

from advent_cli import commands


@patch('builtins.open', new_callable=mock_open())
@patch('requests.get')
def test_get(mock_get, mock_open):
    mock_get.side_effect = [
        MagicMock(text='''
            <meta charset="utf-8">
            <article class="day-desc">
                <h2>--- Day 1: Test ---</h2>
                <p>This is a test puzzle.</p>
            </article>
        '''),
        MagicMock(text='0,1,2,3,4')
    ]
    commands.get('2099', '99')
    mock_open.assert_has_calls([
        call('2099/99/prompt.md', 'w'),
        call().__enter__(),
        call().__enter__().write('\nDay 1: Test\n-----------\n\n\nThis is a ' +
                                 'test puzzle.\n\n\n'),
        call().__exit__(None, None, None),
        call('2099/99/input.txt', 'w'),
        call().__enter__(),
        call().__enter__().write('0,1,2,3,4'),
        call().__exit__(None, None, None),
        call('2099/99/example_input.txt', 'w'),
        call().close(),
        call('2099/99/solution.py', 'w'),
        call().__enter__(),
        call().__enter__().write('## advent of code 2099\n## https://adventofcode.com/2099\n' +
                                 '## day 99\n\ndef parse_input(lines):\n    pass\n\n' +
                                 'def part1(data):\n    pass\n\ndef part2(data):\n    pass'),
        call().__exit__(None, None, None)
    ])
