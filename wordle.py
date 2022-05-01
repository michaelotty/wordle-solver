"""A Wordle solver.

Contains a single function for finding wordle solutions.

Examples:
    >>> wordle(starting_word='rgo',
    ...        greens=['', '', '', '', ''],
    ...        oranges=['g', 'r', 'og', 'o', 'r'],
    ...        blacks='canehul')
    ['borgo', 'forgo', 'porgy', 'sorgo']
"""

import itertools
import json
import logging
import string

FILLER_LETTERS = '-_=+'


def wordle(starting_word: str,
           greens: list[str],
           oranges: list[str],
           blacks: str = None,
           greys: str = None,
           use_word_list: bool = True) -> list[str]:
    """Solve the wordle puzzle.

    Enter all letters you have so far in starting_word, order here does not
    matter. After this, put all green letters that you have in the correct place
    as a list. Or empty character list otherwise. Same again for oranges, you
    can have multiple letters at each place here.
    Lastly, you can either put all black letters in blacks, or if it's easier,
    all the grey letters that haven't been tried in greys.

    Args:
        starting_word: The word we have so far
        greens: An ordered list for each letter, with green letters placement
        oranges: An ordered list for each letter, with orange letter placement
        blacks: A string of all letters that have been ruled out
        grey: All the untried letters
        use_word_list: Whether to check against word list.

    Returns:
        A sorted list of all possible solutions

    Examples:
        >>> wordle(starting_word='rgo',
        ...        greens=['', '', '', '', ''],
        ...        oranges=['g', 'r', 'og', 'o', 'r'],
        ...        blacks='canehul')
        ['borgo', 'forgo', 'porgy', 'sorgo']
    """
    # Normalise input
    starting_word = starting_word.lower()
    greens = [i.lower() for i in greens]
    oranges = [i.lower() for i in oranges]
    blacks = blacks.lower()

    if blacks:
        greys = set(string.ascii_lowercase) - set(blacks)
    elif greys:
        greys = set(greys) | set(''.join(greens)) | set(''.join(oranges))
    else:
        greys = set(string.ascii_lowercase)

    words = set()

    # Append filler letters and trim to word size
    starting_word += FILLER_LETTERS
    starting_word = starting_word[:5]

    grey_letter = ['*'] * 4

    for i, _ in enumerate(grey_letter):
        if FILLER_LETTERS[i] in starting_word:
            grey_letter[i] = greys - set(oranges[i])

    with open('wordle-allowed-guesses.json', encoding='utf-8') as file:
        allowed_words = set(json.load(file))

    for let1 in grey_letter[0]:
        for let2 in grey_letter[1]:
            for let3 in grey_letter[2]:
                for let4 in grey_letter[3]:
                    orange_words = {
                        ''.join(x)
                        for x in itertools.permutations(
                            starting_word.replace('-', let1).replace(
                                '_', let2).replace('=', let3).replace(
                                    '+', let4))
                        if all((a not in b) for a, b in zip(x, oranges))
                    }
                    green_words = {
                        ''.join(x)
                        for x in itertools.permutations(
                            starting_word.replace('-', let1).replace(
                                '_', let2).replace('=', let3).replace(
                                    '+', let4))
                        if all(b in (a, '') for a, b in zip(x, greens))
                    }
                    new_words = orange_words & green_words
                    if use_word_list:
                        new_words &= allowed_words
                    if new_words:
                        logging.info('words added:%s', new_words)

                    words |= new_words

    return sorted(words)
