# 🎄 advent-cli

![](https://img.shields.io/github/v/release/fergusch/advent-cli?color=brightgreen)
![](https://img.shields.io/pypi/v/advent-cli)
![](https://img.shields.io/github/v/tag/fergusch/advent-cli?label=latest)
![](https://img.shields.io/github/workflow/status/fergusch/advent-cli/build?logo=github)
![](https://img.shields.io/github/workflow/status/fergusch/advent-cli/unit%20tests?label=unit%20tests&logo=github)
![](https://img.shields.io/pypi/pyversions/advent-cli)

**advent-cli** is a command-line tool for interacting with [Advent of Code](https://adventofcode.com/), specifically geared toward writing solutions in Python. It can be used to view puzzle prompts, download input, submit solutions, and view personal or private stats and leaderboards.

![](https://user-images.githubusercontent.com/27470183/145635955-5ea316a2-d028-4954-a144-d87846ed05d9.gif)

## Installation
```
pip install advent-cli
```

## Configuration
Before you do anything, you'll need to provide advent-cli with a session cookie so it can authenticate as you. To do this, log in to the [Advent of Code website](https://adventofcode.com/) and grab the cookie named `session` from your browser's inspect element tool. Store it in an environment variable on your machine named `ADVENT_SESSION_COOKIE`. A fresh session cookie is good for about a month, after which you'll need to repeat these steps.

Full list of configuration environment variables:

| Variable                   | Function |
| -------------------------- | -------- |
| `ADVENT_SESSION_COOKIE`    | Advent of Code session cookie for authentication. |
| `ADVENT_PRIV_BOARDS`       | Comma-separated list of private leaderboard IDs. (optional) |
| `ADVENT_DISABLE_TERMCOLOR` | Set to `1` to permanently disable coloring terminal output. (optional) |

## Usage

advent-cli can be invoked using the `advent` command, or `python -m advent_cli`.

### Download a question
```
$ advent get YYYY/DD
```
This will create the directory `YYYY/DD` (e.g. `2021/01`) inside the current working directory. Inside, you'll find part 1 of the puzzle prompt in `prompt.md`, your puzzle input in `input.txt`, and a generated solution template in `solution.py`. More about that [here](#solution-structure).

### Test a solution
```
$ advent test YYYY/DD
```
This will run the solution file in the directory `YYYY/DD` and print the output without actually submitting. Use this to debug or check for correctness. Optional flags:
- `-e`, `--example`: Test the solution using `example_input.txt`. This is an empty file that gets created when you run `advent get` where you can manually store the example input from the puzzle prompt. Useful for checking solutions for correctness before submitting.
- `-f`, `--solution-file`: Test a solution file other than `solution.py` (e.g. `-f solution2` to run `solution2.py`). This will assume you already have a working solution in `solution.py` and check the new file's output against it. Useful for testing alternate solutions after you've already submitted since you cannot re-submit.

### Submit answers
```
$ advent submit YYYY/DD
```
This will run the solution file in the directory `YYYY/DD` and automatically attempt to submit the computed answers for that day. After implementing part 1, run this command to submit part 1 and (if correct) append the prompt for part 2 to `prompt.md`. Run again after implementing part 2 to submit part 2. Optional flags:
- `-f`, `--solution-file`: Submit using a solution file other than `solution.py` (e.g. `-f solution2` to run `solution2.py`). This can only be done if a correct answer hasn't already been submitted.

### Check personal stats
```
$ advent stats YYYY
```
This will print out your progress for the year `YYYY` and output the table found on `adventofcode.com/{YYYY}/leaderboard/self` with your time, rank, and score for each day and part.

### Check private leaderboards
```
$ advent stats YYYY --private
```
This will print out each of the private leaderboards given in `ADVENT_PRIV_BOARDS`. Also works with `-p`.

## Solution structure
advent-cli expects the following directory structure (example):
```
2020/
 └─ 01/
     └─ example_input.txt
     └─ input.txt
     └─ prompt.md
     └─ solution.py
     └─ [alternate solution files]
 └─ 02/
     └─ ...
 └─ ...
2021/
 └─ 01/
     └─ ...
 └─ ...
```

The `solution.py` file will look like this when first generated:
```Python
## advent of code {year}
## https://adventofcode.com/{year}
## day {day}

def parse_input(lines):
    pass

def part1(data):
    pass

def part2(data):
    pass
```
When the solution is run, the input will be read from `input.txt` and automatically passed to `parse_input` as `lines`, an array of strings where each string is a line from the input with newline characters removed. You should implement `parse_input` to return your parsed input or inputs, which will then be passed to `part1` and `part2`. If `parse_input` returns a tuple, `part1` and `part2` will be expecting multiple parameters that map to those returned values. The parameter names can be changed to your liking. The only constraint is that `part1` and `part2` must have the same number of parameters.

If `part2` is left unmodified or otherwise returns `None`, it will be considered unsolved and `part1` will be run and submitted. If both functions are implemented, `part2` will be submitted.

## Changelog
See [Releases](https://github.com/fergusch/advent-cli/releases).

## Credits
This started out as a simple script which was inspired by [Hazel](https://git.bicompact.space/hazel/aoc-2021) and [haskal](https://git.lain.faith/haskal/aoc2020/src/branch/aoc2020/scripts).

## License
advent-cli is distributed under the GNU [GPL-3.0 License](https://github.com/fergusch/advent-cli/blob/main/LICENSE).