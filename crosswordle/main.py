from rich import print
from random import randrange, seed
from dictionary import build_dictionary
from board import Board

def run():
    MAX_GRID_SIZE = 10
    # seed(10)
    
    print("Building dictionary...")
    dictionary = build_dictionary(MAX_GRID_SIZE)
    the_word = dictionary[randrange(0,len(dictionary))]

    print("Building board...")
    board = Board(
        the_word=the_word,
        max_grid_size=MAX_GRID_SIZE
    )

    print("[bold red]Let the games begin")
    while True:
        print(board)
        print(f"Input guess {board.number_guesses+1} word 1...")
        guess_a = input()
        print(f"Input guess {board.number_guesses+1} word 2...")
        guess_b = input()
        exit_code = board.make_a_guess(guess_a, guess_b)
        if exit_code == -1:
            print("[bold red]bad inputs, try again")
        elif exit_code == 1:
            print(f"[bold red]WINNER WINNER[/bold red] [bold yellow]CHEECKEN[/bold yellow] DINNER.\n[bold italic green] You solved the puzzle in {board.number_guesses} guesses!")
            print(board)
            return True
        elif exit_code == 0:
            continue
        else:
            assert False, "SOMETHING BAD HAPPENED"
    

if __name__ == '__main__':
    run()