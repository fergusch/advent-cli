from mock import patch, mock_open, MagicMock
from _mock import mock_get_config

from advent_cli import utils


@patch('advent_cli.config.get_config', mock_get_config)
def test_utils_colored_disabled():
    assert utils.colored('*', 'yellow') == '*'
    assert utils.colored('*', 'cyan') == '/'
    assert utils.colored('*', 'grey') == '.'
    assert utils.colored('text', 'red') == 'text'


@patch('advent_cli.utils.tc_colored')
def test_utils_colored_enabled(mock_tc_colored):
    _ = utils.colored('text', 'red')
    mock_tc_colored.assert_called_once_with('text', 'red')


@patch('builtins.open', mock_open(read_data='1,2,3,4\n5,6,7,8\n'))
@patch('advent_cli.utils.import_module')
def test_compute_answers(mock_import_module):
    mock_import_module.return_value.parse_input.side_effect = \
        lambda l: [[int(x) for x in line.split(',')] for line in l]
    mock_import_module.return_value.part1.side_effect = \
        lambda l: sum([x for line in l for x in line])
    mock_import_module.return_value.part2.side_effect = \
        lambda l: [x for line in l for x in line][-1]
    part1_answer, part2_answer = utils.compute_answers('2099', '99')
    mock_import_module.assert_called_once_with('2099.99.solution')
    assert part1_answer == 36
    assert part2_answer == 8


@patch('requests.post')
def test_submit_answer_pass(mock_post):
    mock_post.return_value.text = "That's the right answer"
    assert utils.submit_answer('2099', '99', '1', '5') == (utils.Status.PASS, None)


@patch('requests.post')
def test_submit_answer_fail(mock_post):
    mock_post.return_value.text = "That's not the right answer"
    assert utils.submit_answer('2099', '99', '1', '5') == (utils.Status.FAIL, None)


@patch('requests.post')
def test_submit_answer_ratelimit(mock_post):
    mock_post.return_value.text = 'You gave an answer too recently'
    assert utils.submit_answer('2099', '99', '1', '5') == (utils.Status.RATE_LIMIT, None)


@patch('requests.post')
def test_submit_answer_completed(mock_post):
    mock_post.return_value.text = 'Did you already complete it?'
    assert utils.submit_answer('2099', '99', '1', '5') == (utils.Status.COMPLETED, None)


@patch('requests.post')
def test_submit_answer_unknown_response(mock_post):
    mock_post.return_value.text = 'Error'
    assert utils.submit_answer('2099', '99', '1', '5') == (utils.Status.UNKNOWN, 'Error')
