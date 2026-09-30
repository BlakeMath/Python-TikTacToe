import contextlib
import importlib.util
import io
from pathlib import Path
import random
import subprocess
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('game', ROOT / 'Tik Tac Toe.py')
game = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(game)


class GameTests(unittest.TestCase):
    def test_all_winning_lines(self):
        for marker in ('X', 'O'):
            for line in game.WINNING_LINES:
                board = game.new_board()
                for position in line:
                    game.place_marker(board, marker, position)
                self.assertTrue(game.win_check(board, marker))
                self.assertFalse(game.win_check(board, 'O' if marker == 'X' else 'X'))

    def test_draw(self):
        board = ['#', 'X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        self.assertTrue(game.full_board_space_check(board))
        self.assertFalse(game.win_check(board, 'X'))
        self.assertFalse(game.win_check(board, 'O'))

    def test_easy_moves_are_legal_and_board_is_unchanged(self):
        board = game.new_board()
        board[5] = 'X'
        original = board[:]
        with patch.object(game.random, 'choice', wraps=random.choice) as choice:
            for _ in range(20):
                self.assertIn(game.computer_choice(board, 'O', 'easy'), game.available_moves(board))
            self.assertEqual(choice.call_count, 20)
        self.assertEqual(board, original)

    def test_hard_never_loses_against_any_human_moves(self):
        for computer in ('X', 'O'):
            human = 'O' if computer == 'X' else 'X'
            for first in (computer, human):
                visited = set()

                def explore(board, turn):
                    key = (tuple(board), turn)
                    if key in visited:
                        return
                    visited.add(key)
                    self.assertFalse(game.win_check(board, human), (computer, first, board))
                    if game.win_check(board, computer) or game.full_board_space_check(board):
                        return
                    original = board[:]
                    moves = [game.computer_choice(board, computer)] if turn == computer else game.available_moves(board)
                    self.assertEqual(board, original)
                    for position in moves:
                        self.assertTrue(game.space_check(board, position))
                        candidate = board[:]
                        candidate[position] = turn
                        explore(candidate, human if turn == computer else computer)

                explore(game.new_board(), first)
                self.assertGreater(len(visited), 100)

    def run_session(self, inputs, first=0):
        output = io.StringIO()
        with patch('builtins.input', side_effect=inputs), patch.object(game.random, 'randrange', return_value=first), contextlib.redirect_stdout(output):
            game.main()
        return output.getvalue()

    def test_two_player_validation_win_replay_and_draw(self):
        output = self.run_session([
            'bad', '2', 'Alice', 'Bob', 'X',
            'abc', '0', '1', '1', '4', '2', '5', '3',
            'bad', 'Y', '1', '2', '3', '5', '4', '6', '8', '7', '9', 'N',
        ])
        for expected in ('Please choose 1 or 2.', 'Please enter a number',
                         'Choose a square between', 'That square is taken',
                         'Alice wins!', 'Round 2', "It's a draw!",
                         'Score: Alice 1  |  Bob 0  |  Draws 1', 'Thanks for playing!'):
            self.assertIn(expected, output)

    def test_computer_sessions_both_difficulties(self):
        for difficulty in ('1', '2'):
            # A perfect opponent responds at 5 and 3, then completes 3-5-7.
            # Easy mode uses the same legal choices to exercise the full UI.
            with patch.object(game.random, 'choice', side_effect=[5, 3, 7]):
                output = self.run_session(['1', difficulty, '', 'X', '1', '2', '4', 'N'])
            self.assertIn('Computer chooses square', output)
            self.assertIn('Computer wins!', output)
            self.assertIn('Score: You 0  |  Computer 1', output)

    def test_quit_and_input_end_exit_cleanly(self):
        self.assertIn('Thanks for playing!', self.run_session(['Q']))
        for exception in (EOFError, KeyboardInterrupt):
            with patch('builtins.input', side_effect=exception), contextlib.redirect_stdout(io.StringIO()) as output:
                game.main()
            self.assertIn('Thanks for playing!', output.getvalue())

    def test_real_terminal_entrypoint_win_and_draw(self):
        cases = [
            ('2\n\n\nX\n1\n4\n2\n5\n3\nN\n', 'wins!'),
            ('2\n\n\nO\n1\n2\n3\n5\n4\n6\n8\n7\n9\nN\n', "It's a draw!"),
        ]
        for inputs, outcome in cases:
            result = subprocess.run([sys.executable, 'Tik Tac Toe.py'], cwd=ROOT,
                                    input=inputs, text=True, capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn(outcome, result.stdout)
            self.assertIn('Thanks for playing!', result.stdout)
            self.assertNotIn('\033[', result.stdout)


if __name__ == '__main__':
    unittest.main()
