# Python Tic Tac Toe

A terminal Tic Tac Toe game for two people or a computer opponent. Uses only the Python standard library.

## Requirements

- Python 3
- A terminal for interactive play

## Run

From the project directory:

```bash
python3 "Tik Tac Toe.py"
```

## Play

1. Choose **Play against the computer** or **Play with a friend**.
2. For computer games, choose **Easy** (random legal moves) or **Unbeatable** (perfect play using minimax).
3. Enter player names, or press Enter to use the defaults.
4. Choose `X` or `O`. The game randomly selects the starting player each round.
5. Choose an empty square from `1` to `9` on your turn. The computer moves automatically.

The first player to complete a row, column, or diagonal wins. A full board without a winner is a draw. Against the unbeatable computer, a draw is the best possible result.

### Board layout

Empty squares show their numbers. X and O use distinct colors in supported terminals; redirected output stays plain. Set `NO_COLOR` to disable colors.

```text
 7 | 8 | 9
---+---+---
 4 | 5 | 6
---+---+---
 1 | 2 | 3
```

### Replay and exit

Enter `Y` after a round to play again with the same players, markers, and difficulty. Wins and draws accumulate in the session score. Enter `N` to finish, or enter `Q` / `quit` at any prompt. Ctrl+C or the end of input also exits cleanly.

## Tests

No additional packages are needed:

```bash
python3 -B -m unittest discover -s tests -v
```

Tests cover winning lines, draws, legal easy moves, every possible human continuation against the unbeatable opponent with both markers and starting players, input validation, replay, computer sessions, and the terminal entry point.
