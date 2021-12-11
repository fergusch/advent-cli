from freezegun import freeze_time
from mock import patch, MagicMock
from _mock import mock_get_config

from advent_cli import commands


@freeze_time('2099-12-03 05:00:00')
@patch('advent_cli.config.get_config', mock_get_config)
@patch('requests.get')
def test_personal_stats(mock_get, capsys):
    mock_get.return_value.text = (
        '<article><pre>'
        '      -------Part 1--------   -------Part 2--------\n'
        'Day       Time  Rank  Score       Time  Rank  Score\n'
        '  3          -     -      -          -     -      -\n'
        '  2   00:00:00     1    100          -     -      -\n'
        '  1   00:00:00     1    100   00:00:00     1    100\n'
        '</pre></article>'
    )
    commands.stats('2099')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == (
        '\n         1111111111222222\n'
        '1234567890123456789012345\n'
        '*/.                       (3*)\n\n'
        '(* 2 stars) (/ 1 star) (. 0 stars)\n\n'
        '           ----    (Part 1)     ----      ----    (Part 2)     ----\n'
        '  Day      Time        Rank    Score      Time        Rank    Score\n'
        '-----  --------  ----------  -------  --------  ----------  -------\n'
        '    3         -           -        -         -           -        -\n'
        '    2  00:00:00           1      100         -           -        -\n'
        '    1  00:00:00           1      100  00:00:00           1      100 \n\n'
        'You are a member of 1 private leaderboard(s).\n'
        'Use "advent stats 2099 --private" to see them.\n\n'
    )


@freeze_time('2099-12-03 05:00:00')
@patch('advent_cli.config.get_config', mock_get_config)
@patch('requests.get')
def test_private_stats(mock_get, capsys):
    mock_get.side_effect = [
        MagicMock(text=(
            '<article><p>'
            'This is the private leaderboard of example for Advent of Code 2099.'
            '</p><div class="privboard-row"></div>'
            '<div class="privboard-row">'
            '<span class="privboard-position"> 1)</span>99'
            '<span class="privboard-star-both">*</span>'
            '<span class="privboard-star-firstonly">*</span>'
            '<span class="privboard-star-unlocked">*</span>' +
            '<span class="privboard-star-locked">*</span>'*22 +
            '<span class="privboard-name">'
            '<a href="https://github.com/example">example</a>'
            '</span>'
            '</div><div class="privboard-row">'
            '<span class="privboard-position"> 2)</span>92'
            '<span class="privboard-star-both">*</span>'
            '<span class="privboard-star-unlocked">*</span>'
            '<span class="privboard-star-unlocked">*</span>' +
            '<span class="privboard-star-locked">*</span>'*22 +
            '<span class="privboard-name">example2</span>'
            '</article>'
        )),
    ]
    commands.private_leaderboard_stats('2099')
    captured_stdout = capsys.readouterr().out
    assert captured_stdout == (
        '\nexample\'s private leaderboard (1111111)\n\n'
        '                1111111111222222\n'
        '       1234567890123456789012345\n'
        ' 1) 99 */.                       example (https://github.com/example)\n'
        ' 2) 92 *..                       example2 \n\n'
        '(* 2 stars) (/ 1 star) (. 0 stars)\n\n'
    )
