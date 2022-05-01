"""A Wordle solver.

Contains a single function for finding wordle solutions.

Examples:
    >>> solve(
    ...       WordleData(starting_word='rgo',
    ...                  greens=['', '', '', '', ''],
    ...                  oranges=['g', 'r', 'og', 'o', 'r'],
    ...                  blacks='canehul'))
    ['borgo', 'forgo', 'porgy', 'sorgo']
"""

from dataclasses import dataclass
import itertools
import json
import logging
import string

FILLER_LETTERS = '-_=+'


@dataclass(kw_only=True)
class WordleData:
    """Wordle data for solver.

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
    """
    starting_word: str
    greens: list[str]
    oranges: list[str]
    blacks: str = None
    greys: str = None

    def __post_init__(self):
        """Normalise input."""
        self.starting_word = self.starting_word.lower()
        self.greens = [i.lower() for i in self.greens]
        self.oranges = [i.lower() for i in self.oranges]
        self.blacks = self.blacks.lower()

        # Append filler letters and trim to word size
        self.starting_word += FILLER_LETTERS
        self.starting_word = self.starting_word[:5]


def solve(wordle_data: WordleData, use_word_list: bool = True) -> list[str]:
    """Solve the wordle puzzle.

    Enter the wordle data, and optionally use word list.

    Args:
        wordle_data: All the neccesery wordle data
        use_word_list: Whether to check against word list.

    Returns:
        A sorted list of all possible solutions

    Examples:
        >>> solve(
        ...       WordleData(starting_word='rgo',
        ...                  greens=['', '', '', '', ''],
        ...                  oranges=['g', 'r', 'og', 'o', 'r'],
        ...                  blacks='canehul'))
        ['borgo', 'forgo', 'porgy', 'sorgo']
    """
    if wordle_data.blacks:
        greys = set(string.ascii_lowercase) - set(wordle_data.blacks)
    elif greys:
        greys = set(greys) | set(''.join(wordle_data.greens)) | set(''.join(
            wordle_data.oranges))
    else:
        greys = set(string.ascii_lowercase)

    words = set()

    grey_letter = ['*'] * 4

    for i, _ in enumerate(grey_letter):
        if FILLER_LETTERS[i] in wordle_data.starting_word:
            grey_letter[i] = greys - set(wordle_data.oranges[i])

    with open('wordle-allowed-guesses.json', encoding='utf-8') as file:
        allowed_words = set(json.load(file))

    let = [None] * 4

    for let[0] in grey_letter[0]:
        for let[1] in grey_letter[1]:
            for let[2] in grey_letter[2]:
                for let[3] in grey_letter[3]:
                    new_words = {  # Orange words
                        ''.join(x)
                        for x in itertools.permutations(
                            wordle_data.starting_word.replace('-', let[0]).
                            replace('_', let[1]).replace('=', let[2]).replace(
                                '+', let[3])) if all(
                                    (a not in b)
                                    for a, b in zip(x, wordle_data.oranges))
                    } & {  # Green words
                        ''.join(x)
                        for x in itertools.permutations(
                            wordle_data.starting_word.replace(
                                '-', let[0]).replace('_', let[1]).replace(
                                    '=', let[2]).replace('+', let[3]))
                        if all(b in (a, '')
                               for a, b in zip(x, wordle_data.greens))
                    }
                    if use_word_list:
                        new_words &= allowed_words
                    if new_words:
                        logging.info('words added:%s', new_words)

                    words |= new_words

    return sorted(words)
