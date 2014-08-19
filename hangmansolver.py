import re
import string
import operator
from words import words

class HangmanSolver(object):
    """Hangman AI solver class."""

    def __init__(self, letter_count):
        """
        Initialise the game.

        letter_count: integer representing number of letters in the word
        """
        self._letter_count = letter_count
        self._guessed_letters = []
        self._word_letters = [None] * letter_count
        self._words_list = words

    @staticmethod
    def _filter_matched_words(words_list, word_letters):
        regex_s = HangmanSolver._word_letters_to_regex_s(word_letters)
        regex = re.compile(regex_s)
        return filter(regex.search, words_list)

    @staticmethod
    def _get_most_popular_chars(words_list):
        chars_dict = {}

        for word in words_list:
            for char in string.lowercase:
                if char in word:
                    if char in chars_dict:
                        chars_dict[char] += 1
                    else:
                        chars_dict[char] = 1

        sorted_chars_dict = sorted(chars_dict.iteritems(),
            key=operator.itemgetter(1), reverse=True)

        chars = []

        for char_tuple in sorted_chars_dict:
            chars.append(char_tuple[0])

        return chars

    @staticmethod
    def _word_letters_to_regex_s(word_letters):
        regexp = '^'

        for letter in word_letters:
            if letter is None:
                regexp += '.'
            else:
                regexp += letter.lower()

        regexp += '$'

        return regexp

    def get_next_move(self):
        """Returns the letter that should be played next."""
        self._words_list = HangmanSolver._filter_matched_words(
            self._words_list, self._word_letters)

        chars = HangmanSolver._get_most_popular_chars(self._words_list)

        print chars

    def guess_letter(self, letter):
        """Add a new guessed letter."""
        self._guessed_letters.append(letter)

    def set_word_letters(self, word_letters):
        """Set a new word state."""
        self._word_letters = word_letters
