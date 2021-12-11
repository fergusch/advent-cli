from mock import patch, call, mock_open
from _fixtures import env_patch_fixture

from advent_cli import commands
from advent_cli.utils import Status


@patch('advent_cli.commands.compute_answers', return_value=(None, None))
@patch('os.path.exists', return_value=True)
def test_submit_no_solution(mock_exists, mock_compute, capsys):
    commands.submit('2099', '99')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == 'No solution implemented\n'


@patch('builtins.open', new_callable=mock_open())
@patch('requests.get')
@patch('advent_cli.commands.submit_answer', return_value=(Status.PASS, None))
@patch('advent_cli.commands.compute_answers', return_value=(5, None))
@patch('os.path.exists', return_value=True)
def test_submit_part1(mock_exists, mock_compute, mock_submit, mock_get,
                      mock_open, capsys):
    mock_get.return_value.text = '''
            <meta charset="utf-8">
            <article class="day-desc"></article>
            <article class="day-desc">
                <h2>--- Part Two ---</h2>
                <p>This is part 2.</p>
            </article>
        '''
    commands.submit('2099', '99')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == ('Submitting part 1...\n'
                               'Correct! /\n'
                               'Appended part 2 prompt to 2099/99/prompt.md\n')
    mock_open.assert_has_calls([
        call('2099/99/prompt.md', 'a'),
        call().__enter__().write(
            '\nPart Two\n--------\n\n\nThis is part 2.\n\n\n'
        ),
    ], any_order=True)


@patch('advent_cli.commands.submit_answer', return_value=(Status.PASS, None))
@patch('advent_cli.commands.compute_answers', return_value=(5, 10))
@patch('os.path.exists', return_value=True)
def test_submit_part2(mock_exists, mock_compute, mock_submit, capsys):
    commands.submit('2099', '99')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == ('Submitting part 2...\n'
                               'Correct! **\n'
                               'Day 99 complete!\n')


@patch('advent_cli.commands.submit_answer', return_value=(Status.PASS, None))
@patch('advent_cli.commands.compute_answers', return_value=(5, 10))
@patch('os.path.exists', return_value=True)
def test_submit_altsoln(mock_exists, mock_compute, mock_submit, capsys):
    commands.submit('2099', '99', solution_file='solution2')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == ('(Using solution2.py)\n'
                               'Submitting part 2...\n'
                               'Correct! **\n'
                               'Day 99 complete!\n')


@patch('builtins.open', new_callable=mock_open())
@patch('os.getcwd', return_value='/fake/path')
@patch('os.path.exists', side_effect=[True, False])
def test_submit_altsoln_nofile(mock_exists, mock_getcwd, mock_open, capsys):
    commands.submit('2099', '99', solution_file='solution2')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == ('Solution file does not exist:\n'
                               '  "/fake/path/2099/99/solution2.py"\n')
    mock_open.assert_not_called()


@patch('builtins.open', new_callable=mock_open())
@patch('os.getcwd', return_value='/fake/path')
@patch('os.path.exists', return_value=False)
def test_submit_no_dir(mock_exists, mock_getcwd, mock_open, capsys):
    commands.submit('2099', '99')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == ('Directory does not exist:\n'
                               '  "/fake/path/2099/99/"\n')
    mock_open.assert_not_called()
