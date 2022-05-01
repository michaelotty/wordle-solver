# Wordle Solver

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/michaelotty/wordle-solver)](https://github.com/michaelotty/wordle-solver/releases/latest)
[![GitHub](https://img.shields.io/github/license/michaelotty/wordle-solver)](https://raw.githubusercontent.com/michaelotty/wordle-solver/master/LICENSE)
[![GitHub branch checks state](https://img.shields.io/github/checks-status/michaelotty/wordle-solver/master)](https://github.com/michaelotty/wordle-solver/tree/master)
[![Python application](https://github.com/michaelotty/wordle-solver/actions/workflows/python-app.yml/badge.svg)](https://github.com/michaelotty/wordle-solver/actions/workflows/python-app.yml)

Computes a list of all wordle puzzle possibilities.

## Example

```
words = wordle(starting_word='rgo',
               greens=['', '', '', '', ''],
               oranges=['g', 'r', 'og', 'o', 'r'],
               blacks='canehul',
               use_word_list=True)
print(*words, sep=', ')
```
