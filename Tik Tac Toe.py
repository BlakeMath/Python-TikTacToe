"""A terminal Tic Tac Toe game for two people or a computer opponent."""

from functools import lru_cache
import os
import random
import sys


WINNING_LINES = (
    (7, 8, 9), (4, 5, 6), (1, 2, 3),
    (7, 4, 1), (8, 5, 2), (9, 6, 3),
    (7, 5, 3), (9, 5, 1),
)


def styled(text, color):
    """Keep redirected output and NO_COLOR terminals free of ANSI codes."""
    if sys.stdout.isatty() and 'NO_COLOR' not in os.environ:
        return f'\033[{color}m{text}\033[0m'
    return text


def new_board():
    return ['#'] + [str(position) for position in range(1, 10)]


def display_board(board):
    print()
    for row, positions in enumerate(((7, 8, 9), (4, 5, 6), (1, 2, 3))):
        cells = [styled(board[p], '36' if board[p] == 'X' else '33' if board[p] == 'O' else '2') for p in positions]
        print('    ' + ' | '.join(cells))
        if row < 2:
            print('   ---+---+---')
    print()


def place_marker(board, marker, position):
    board[position] = marker


def win_check(board, mark):
    return any(all(board[p] == mark for p in line) for line in WINNING_LINES)


def space_check(board, position):
    return board[position] not in ('X', 'O')


def available_moves(board):
    return [p for p in range(1, 10) if space_check(board, p)]


def full_board_space_check(board):
    return not available_moves(board)


@lru_cache(maxsize=None)
def minimax(board, turn, computer):
    """Score a position from the computer's perspective using perfect play."""
    human = 'O' if computer == 'X' else 'X'
    if win_check(board, computer):
        return 1
    if win_check(board, human):
        return -1
    moves = available_moves(board)
    if not moves:
        return 0
    scores = []
    for position in moves:
        candidate = list(board)
        candidate[position] = turn
        scores.append(minimax(tuple(candidate), 'O' if turn == 'X' else 'X', computer))
    return max(scores) if turn == computer else min(scores)


def computer_choice(board, marker, difficulty='hard'):
    moves = available_moves(board)
    if not moves:
        raise ValueError('The board has no available moves.')
    if difficulty == 'easy':
        return random.choice(moves)
    if difficulty != 'hard':
        raise ValueError('Difficulty must be easy or hard.')
    opponent = 'O' if marker == 'X' else 'X'

    def score(position):
        candidate = list(board)
        candidate[position] = marker
        return minimax(tuple(candidate), opponent, marker)

    # Prefer the center and corners when several moves have the same score.
    preferred = [p for p in (5, 7, 9, 1, 3, 8, 4, 6, 2) if p in moves]
    return max(preferred, key=score)


def read_input(prompt):
    answer = input(prompt).strip()
    if answer.lower() in ('q', 'quit'):
        raise EOFError
    return answer


def select_option(prompt, options):
    while True:
        answer = read_input(prompt).upper()
        if answer in options:
            return answer
        print('Please choose ' + ' or '.join(options) + '.')


def player_choice(board):
    while True:
        try:
            position = int(read_input('  Choose a square (1-9): '))
        except ValueError:
            print('  Please enter a number between 1 and 9.')
            continue
        if position not in range(1, 10):
            print('  Choose a square between 1 and 9.')
        elif not space_check(board, position):
            print('  That square is taken. Try another one.')
        else:
            return position


def main():
    print(styled('\n  TIC TAC TOE', '1;36'))
    print('  Choose a numbered square to place your marker. Enter Q anytime to quit.\n')
    try:
        print('  1. Play against the computer\n  2. Play with a friend')
        mode = select_option('  Game mode (1/2): ', ('1', '2'))
        difficulty = None
        if mode == '1':
            print('\n  1. Easy — random moves\n  2. Unbeatable — perfect play')
            difficulty = 'easy' if select_option('  Difficulty (1/2): ', ('1', '2')) == '1' else 'hard'
            names = [read_input('  Your name [You]: ') or 'You', 'Computer']
        else:
            names = [read_input('  Player 1 name [Player 1]: ') or 'Player 1',
                     read_input('  Player 2 name [Player 2]: ') or 'Player 2']
        marker = select_option(f'  {names[0]}, choose your marker (X/O): ', ('X', 'O'))
        markers = [marker, 'O' if marker == 'X' else 'X']
        scores = [0, 0]
        draws = 0
        round_number = 1
        while True:
            board = new_board()
            turn = random.randrange(2)
            print(styled(f'\n  Round {round_number}  |  {names[0]} ({markers[0]}) vs {names[1]} ({markers[1]})', '1'))
            print(f'  {names[turn]} goes first.')
            while True:
                display_board(board)
                print(f'  {names[turn]}\'s turn ({markers[turn]})')
                if mode == '1' and turn == 1:
                    position = computer_choice(board, markers[turn], difficulty)
                    print(f'  Computer chooses square {position}.')
                else:
                    position = player_choice(board)
                place_marker(board, markers[turn], position)
                if win_check(board, markers[turn]):
                    display_board(board)
                    print(styled(f'  {names[turn]} wins!', '1;32'))
                    scores[turn] += 1
                    break
                if full_board_space_check(board):
                    display_board(board)
                    print(styled("  It's a draw!", '1;33'))
                    draws += 1
                    break
                turn = 1 - turn
            print(f'  Score: {names[0]} {scores[0]}  |  {names[1]} {scores[1]}  |  Draws {draws}')
            if select_option('\n  Play again? (Y/N): ', ('Y', 'N')) == 'N':
                break
            round_number += 1
    except (EOFError, KeyboardInterrupt):
        print()
    print('  Thanks for playing!')


if __name__ == '__main__':
    main()
