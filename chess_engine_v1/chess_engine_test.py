import unittest

import fen
from board import Board
from chess_engine import ChessEngine, uci_algebraic_notation
from move import Move
from square import Squares


class TestChessEngine(unittest.TestCase):
    def test_evaluate(self) -> None:
        board = Board(fen.STARTING_GAME_FEN)
        engine = ChessEngine(board)
        # Test the evaluation function
        self.assertEqual(engine.evaluate(), 0)  # Initial position is balanced

        # Test a board with a material imbalance
        board.board[4][4] = "Q"  # Add a white queen in the center
        self.assertEqual(engine.evaluate(), 9)

    def test_best_move(self) -> None:
        # White has a pawn that can't move and a king in the corner that can only move
        # to one square. So there is only one move white can make.
        fen_str = "8/8/8/8/7k/7p/7P/7K w - - 0 1"
        board = Board(fen_str)
        engine = ChessEngine(board)

        # Test the best move function
        move = engine.best_move(1)
        expected_move = Move(Squares.H1, Squares.G1, "K")
        self.assertEqual(move, expected_move)


class TestUCIAlgebraicNotation(unittest.TestCase):
    def test_uci_algebraic_notation_white(self) -> None:
        move = Move(Squares.E2, Squares.E4, "P")
        self.assertEqual(uci_algebraic_notation(move), "e2e4")

        move = Move(Squares.E2, Squares.E4, "R")
        self.assertEqual(uci_algebraic_notation(move), "e2e4")

        move = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        self.assertEqual(uci_algebraic_notation(move), "e7e8q")

    def test_uci_algebraic_notation_black(self) -> None:
        move = Move(Squares.E7, Squares.E5, "p")
        self.assertEqual(uci_algebraic_notation(move), "e7e5")

        move = Move(Squares.E7, Squares.E5, "r")
        self.assertEqual(uci_algebraic_notation(move), "e7e5")

        move = Move(Squares.E2, Squares.E1, "p", promotion_piece="q")
        self.assertEqual(uci_algebraic_notation(move), "e2e1q")


if __name__ == "__main__":
    unittest.main()
