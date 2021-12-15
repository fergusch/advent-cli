from mock import patch
from _fixtures import env_patch_fixture

from advent_cli import cli


@patch('advent_cli.cli.commands.get')
@patch('argparse.ArgumentParser')
def test_cli_get(mock_argparse, mock_command_get):
    mock_argparse.return_value.parse_args.return_value.date = '2099/99'
    mock_argparse.return_value.parse_args.return_value.command = 'get'
    cli.main()
    mock_command_get.assert_called_once_with('2099', '99')


@patch('advent_cli.cli.commands.stats')
@patch('argparse.ArgumentParser')
def test_cli_stats(mock_argparse, mock_command_stats):
    mock_argparse.return_value.parse_args.return_value.year = '2099'
    mock_argparse.return_value.parse_args.return_value.command = 'stats'
    mock_argparse.return_value.parse_args.return_value.show_private = False
    cli.main()
    mock_command_stats.assert_called_once_with('2099')


@patch('advent_cli.cli.commands.private_leaderboard_stats')
@patch('argparse.ArgumentParser')
def test_cli_stats_private(mock_argparse, mock_command_stats):
    mock_argparse.return_value.parse_args.return_value.year = '2099'
    mock_argparse.return_value.parse_args.return_value.command = 'stats'
    mock_argparse.return_value.parse_args.return_value.show_private = True
    cli.main()
    mock_command_stats.assert_called_once_with('2099')


@patch('advent_cli.cli.commands.test')
@patch('argparse.ArgumentParser')
def test_cli_test(mock_argparse, mock_command_test):
    mock_argparse.return_value.parse_args.return_value.date = '2099/99'
    mock_argparse.return_value.parse_args.return_value.command = 'test'
    mock_argparse.return_value.parse_args.return_value.solution_file = 'solution'
    mock_argparse.return_value.parse_args.return_value.run_example = False
    cli.main()
    mock_command_test.assert_called_once_with('2099', '99', solution_file='solution',
                                              example=False)


@patch('advent_cli.cli.commands.submit')
@patch('argparse.ArgumentParser')
def test_cli_submit(mock_argparse, mock_command_submit):
    mock_argparse.return_value.parse_args.return_value.date = '2099/99'
    mock_argparse.return_value.parse_args.return_value.command = 'submit'
    mock_argparse.return_value.parse_args.return_value.solution_file = 'solution'
    cli.main()
    mock_command_submit.assert_called_once_with('2099', '99', solution_file='solution')


@patch('advent_cli.cli.commands.countdown')
@patch('argparse.ArgumentParser')
def test_cli_countdown(mock_argparse, mock_command_submit):
    mock_argparse.return_value.parse_args.return_value.date = '2099/99'
    mock_argparse.return_value.parse_args.return_value.command = 'countdown'
    cli.main()
    mock_command_submit.assert_called_once_with('2099', '99')
