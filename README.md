# Wordle Solver

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
