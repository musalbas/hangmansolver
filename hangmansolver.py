class HangmanSolver:
    """Hangman AI solver class."""

    def __init__(self, letter_count):
        """
        Initialise the game.

        letter_count: integer representing number of letters in the word
        """
        self._letter_count = letter_count
        self._guessed_letters = []
        self._word_letters = [None] * letter_count

    def get_next_move(self):
        """Returns the letter that should be played next."""
        return HangmanSolver.get_next_move_by_state(self._word_letters,
            self._guessed_letters)

    def get_next_move_by_state(word_letters, guessed_letters):
        """Returns the letter that should be played next (static method)."""
        pass

    def guess_letter(self, letter):
        """Add a new guessed letter."""
        self._guessed_letters.append(letter)

    def set_word_letters(self, word_letters):
        """Set a new word state."""
        self._word_letters = word_letters
