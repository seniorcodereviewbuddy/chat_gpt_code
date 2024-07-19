import unittest

from move import Move
from square import Squares


class TestMove(unittest.TestCase):
    def test_move_initialization(self) -> None:
        move = Move(Squares.E2, Squares.E4, "P", "p")
        self.assertEqual(move.start, Squares.E2)
        self.assertEqual(move.end, Squares.E4)
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, "p")
        self.assertIsNone(move.promotion_piece)

    def test_move_initialization_with_promotion(self) -> None:
        move = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        self.assertEqual(move.start, Squares.E7)
        self.assertEqual(move.end, Squares.E8)
        self.assertEqual(move.piece_moved, "P")
        self.assertEqual(move.piece_captured, None)
        self.assertEqual(move.promotion_piece, "Q")

    def test_move_str(self) -> None:
        move = Move(Squares.E2, Squares.E4, "P", "p")
        self.assertEqual(str(move), "P from e2 to e4, capturing p")

    def test_move_str_with_promotion(self) -> None:
        move = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        self.assertEqual(str(move), "P from e7 to e8, promoting to Q")

    def test_move_repr(self) -> None:
        move = Move(Squares.E2, Squares.E4, "P", "p")
        self.assertEqual(repr(move), "P from e2 to e4, capturing p")

    def test_move_repr_with_promotion(self) -> None:
        move = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        self.assertEqual(repr(move), "P from e7 to e8, promoting to Q")

    def test_move_equality(self) -> None:
        move1 = Move(Squares.E2, Squares.E4, "P", "p")
        move2 = Move(Squares.E2, Squares.E4, "P", "p")
        self.assertEqual(move1, move2)

    def test_move_inequality(self) -> None:
        move1 = Move(Squares.E2, Squares.E4, "P", "p")
        move2 = Move(Squares.D2, Squares.D4, "P", "p")
        self.assertNotEqual(move1, move2)

    def test_move_inequality_same_piece_and_squares_other_player(self) -> None:
        move1 = Move(Squares.E2, Squares.E4, "R")
        move2 = Move(Squares.E2, Squares.E4, "r")
        self.assertNotEqual(move1, move2)

    def test_move_inequality_with_promotion(self) -> None:
        move1 = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        move2 = Move(Squares.E7, Squares.E8, "P", promotion_piece="R")
        self.assertNotEqual(move1, move2)

    def test_move_hash(self) -> None:
        move1 = Move(Squares.E2, Squares.E4, "P", "p")
        move2 = Move(Squares.E2, Squares.E4, "P", "p")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)

    def test_move_hash_with_promotion(self) -> None:
        move1 = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        move2 = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        move_set = {move1, move2}
        self.assertEqual(len(move_set), 1)


if __name__ == "__main__":
    unittest.main()
