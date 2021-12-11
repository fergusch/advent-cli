from mock import patch, call, mock_open, MagicMock
from _fixtures import env_patch_fixture

from advent_cli import commands


@patch('os.makedirs')
@patch('builtins.open', new_callable=mock_open())
@patch('requests.get')
def test_get(mock_get, mock_open, mock_mkdir):
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
        call('2099/99/input.txt', 'w'),
        call('2099/99/example_input.txt', 'w'),
        call('2099/99/solution.py', 'w'),
    ], any_order=True)
    mock_open.assert_has_calls([
        call().__enter__().write(
            '\nDay 1: Test\n-----------\n\n\nThis is a test puzzle.\n\n\n'
        ),
        call().__enter__().write('0,1,2,3,4'),
        call().__enter__().write(
            ('## advent of code 2099\n## https://adventofcode.com/2099\n'
             '## day 99\n\ndef parse_input(lines):\n    pass\n\n'
             'def part1(data):\n    pass\n\ndef part2(data):\n    pass')
        )
    ], any_order=True)
    mock_mkdir.assert_called_once_with('2099/99/')


@patch('builtins.open', new_callable=mock_open())
@patch('os.path.exists')
def test_get_path_exists(mock_exists, mock_open):
    mock_exists.side_effect = lambda x: {'2099/99/': True}[x]
    commands.get('2099', '99')
    mock_open.assert_not_called()


@patch('builtins.open', new_callable=mock_open())
@patch('requests.get')
def test_get_puzzle_locked(mock_get, mock_open):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = ('Please don\'t repeatedly request '
                                  'this endpoint before it unlocks!')
    commands.get('2099', '99')
    mock_open.assert_not_called()


@patch('builtins.open', new_callable=mock_open())
@patch('requests.get')
def test_get_404(mock_get, mock_open):
    mock_get.return_value.status_code = 404
    mock_get.return_value.text = '404 Not Found'
    commands.get('2099', '99')
    mock_open.assert_not_called()
