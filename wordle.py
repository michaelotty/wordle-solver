"""Wordle solver."""

import json
import itertools
import string


def wordle(starting_word: str,
           ins: list[str],
           not_ins: list[str],
           black: str,
           grey: str = string.ascii_lowercase) -> list[str]:
    """Solve the wordle puzzle.

    Args:
        starting_word: The word we have so far
        grey: All avaliable letters including green and amber ones

    Returns:
        A list of all possible solutions
    """
    if black:
        grey = set(grey) - set(black)
    words = set()
    starting_word = starting_word + '-_=+'
    starting_word = starting_word[:5]
    for letter1, letter2, letter3 in itertools.product(grey, repeat=3):
        words |= {
            ''.join(x)
            for x in itertools.permutations(
                starting_word.replace('-', letter1).replace('_', letter2).
                replace('=', letter3))  # .replace('+', letter4))
            if any(
                ((a in b) or (a not in c)) for a, b, c in zip(x, ins, not_ins))
        }
    with open('wordle-allowed-guesses.json', encoding='utf-8') as file:
        allowed_words = set(json.load(file))

    return sorted(words & allowed_words)


if __name__ == "__main__":
    print(
        wordle(starting_word='au',
               ins=['', '', '', '', ''],
               not_ins=['', '', 'a', 'u', ''],
               black='eroghlcn'))
