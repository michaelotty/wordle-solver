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

    filler_letters = '-_=+'

    starting_word = starting_word + filler_letters
    starting_word = starting_word[:5]
    grey_letter = ['*', '*', '*', '*']

    for i, _ in enumerate(grey_letter):
        if filler_letters[i] in starting_word:
            grey_letter[i] = grey

    for let1 in grey_letter[0]:
        for let2 in grey_letter[1]:
            for let3 in grey_letter[2]:
                for let4 in grey_letter[3]:
                    words |= {
                        ''.join(x)
                        for x in itertools.permutations(
                            starting_word.replace('-', let1).replace(
                                '_', let2).replace('=', let3).replace(
                                    '+', let4))
                        if all(((a in b) or (a not in c))
                               for a, b, c in zip(x, ins, not_ins))
                    }

    with open('wordle-allowed-guesses.json', encoding='utf-8') as file:
        allowed_words = set(json.load(file))

    return sorted(words & allowed_words)


if __name__ == "__main__":
    print(*wordle(starting_word='rali',
                  ins=['', '', 'a', '', ''],
                  not_ins=['', 'r', '', '', 'l'],
                  black='cneghous'),
          sep=', ')
