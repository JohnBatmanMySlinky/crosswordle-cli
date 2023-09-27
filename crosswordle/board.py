from rich import print
from dataclasses import dataclass

@dataclass
class AnalyzedGuess:
    word_a: list[str]
    word_b: list[str]

class Board:
    def __init__(self, the_word: dict, max_grid_size: int = 10):
        self.the_word = the_word
        self.max_grid_size = max_grid_size
        self.number_guesses = 0
        self._build_board()
        self._build_header()

    def make_a_guess(self, guess_a: str, guess_b: str) -> tuple:
        # first validate input
        validation_check, error_msg = self._validate_guess(guess_a, guess_b)
        if validation_check == False:
            # if we dont pass validation, exit early with a -1
            return -1, error_msg
        
        # we have passed validation, continuing
        self.number_guesses += 1
        analyzed_guess = self._analyze_guess(guess_a, guess_b)
        self._update_header(analyzed_guess)
        self._update_board(analyzed_guess)

        # if we have a winner, exit early with a 1
        winner_check = self._check_for_winner(guess_a, guess_b)
        if winner_check == True:
            return 1, ""
        
        # else, continue
        return 0, ""

    def _analyze_guess(self, guess_a: str, guess_b: str) -> dict:
        # store a list of formatted strings
        # TODO actually put in the crosswordle rules here...
        analyzed_guess = AnalyzedGuess([], [])

        for a, (guessed_letter, word_letter) in enumerate(zip(guess_a, self.the_word.word_a)):
            if guessed_letter == word_letter:
                analyzed_guess.word_a.append(f"[green bold]{guessed_letter}[/green bold]")
            elif guessed_letter in self.the_word.word_a:
                analyzed_guess.word_a.append(f"[yellow bold]{guessed_letter}[/yellow bold]")
            else:
                analyzed_guess.word_a.append(guessed_letter)

        for b, (guessed_letter, word_letter) in enumerate(zip(guess_b, self.the_word.word_b)):
            if guessed_letter == word_letter:
                analyzed_guess.word_b.append(f"[green bold]{guessed_letter}[/green bold]")
            elif guessed_letter in self.the_word.word_a:
                analyzed_guess.word_b.append(f"[yellow bold]{guessed_letter}[/yellow bold]")
            else:
                analyzed_guess.word_b.append(guessed_letter)

        return analyzed_guess

    def _update_board(self, analyzed_guess: dict) -> None:
        # run thru analyzed guesses and put letters on board
        for a, letter_formatted in enumerate(analyzed_guess.word_a):
            if "green" in letter_formatted:
                self.board[self.the_word.index_b][a] = letter_formatted

        for b, letter_formatted in enumerate(analyzed_guess.word_b):
            if "green" in letter_formatted:
                self.board[b][self.the_word.index_a] = letter_formatted
        
    def _check_for_winner(self, guess_a: str, guess_b: str) -> bool:
        if (guess_a == self.the_word.word_a) & (guess_b == self.the_word.word_b):
            return True
        else:
            return False

    def _validate_guess(self, guess_a: str, guess_b: str) -> None:
        problems = []
        check = True

        # checks that apply to both guesses equally
        for i, (guess, truth) in enumerate(zip([guess_a, guess_b], [self.the_word.word_a, self.the_word.word_b])):
            if not guess.isalpha():
                problems.append(f"   -symbols in guess {i+1}")
                check = False

            if not len(guess) == len(truth):
                problems.append(f"   -guess {i+1} is the wrong length")
                check = False

        # additional check to enforce that overlapping letter is the same!!!
        if guess_a[self.the_word.index_a] != guess_b[self.the_word.index_b]:
            check = False
            problems.append("   -overlapping letter must be the same in both guesses")
        
        return check, "\n".join(problems)

    def _update_header(self, analyzed_guess: dict) -> None:
        # take strings for analyzed guess and concat into a single string
        guess_a_formatted = "".join(analyzed_guess.word_a)
        guess_b_formatted = "".join(analyzed_guess.word_b)
        
        # append guesses to header string
        self.header += f"Guess {self.number_guesses}: {guess_a_formatted} {guess_b_formatted}\n"

    def _build_board(self) -> None:
        # first build an emtpy board of only spaces
        self.board = [list(" "*self.max_grid_size) for i in range(self.max_grid_size)]

        # for word a fill in blank tiles
        for a, _ in enumerate(self.the_word.word_a):
            self.board[self.the_word.index_b][a] = "█"

        # for word b fill in blank tiles
        for b, _ in enumerate(self.the_word.word_b):
            self.board[b][self.the_word.index_a] = "█"

    def _build_header(self) -> None:
        # instantiating empty header, this gets filled up with guesses
        self.header = "\n\n"

    def __rich__(self) -> str:
        # format the board into a nice string for rich
        return self.header + "\n".join([" ".join(self.board[i]) for i in range(self.max_grid_size)])
    