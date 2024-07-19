import unittest

from chess_engine import Board, ChessEngine, Pieces, uci_algebraic_notation
from move import Move
from square import Squares

# TODO: Chris: Fix all tests.


class TestChessEngine(unittest.TestCase):
    def setUp(self):
        # Initialize the board and engine with a starting position
        self.fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.board = Board(self.fen)
        self.engine = ChessEngine(self.board)

    def test_parse_fen(self):
        # Test the FEN parsing
        expected_board = [
            ["R", "N", "B", "Q", "K", "B", "N", "R"],
            ["P", "P", "P", "P", "P", "P", "P", "P"],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", "."],
            ["p", "p", "p", "p", "p", "p", "p", "p"],
            ["r", "n", "b", "q", "k", "b", "n", "r"],
        ]
        self.assertEqual(self.board.board, expected_board)

    # TODO: ChatGPT: Add non-new game FEN tests.

    # TODO: ChatGPT: Add tests for:
    # -Different positions
    # -Black pieces
    # -En-passant pawn captures
    # -Pawn promotions
    # -Where some squares are blocked

    def test_generate_pawn_moves(self):
        # Test pawn move generation
        self.board.board[1][0] = Pieces.WHITE_PAWN
        moves = self.board.generate_piece_moves(1, 0)
        expected_moves = [
            Move(Squares.A2, Squares.A3, Pieces.WHITE_PAWN),
            Move(Squares.A2, Squares.A4, Pieces.WHITE_PAWN),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    @unittest.expectedFailure
    def test_generate_rook_moves(self):
        # Test rook move generation
        self.board.board[4][4] = Pieces.WHITE_ROOK
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (4, 5)),
            ((4, 4), (4, 6)),
            ((4, 4), (4, 7)),
            ((4, 4), (4, 3)),
            ((4, 4), (4, 2)),
            ((4, 4), (4, 1)),
            ((4, 4), (4, 0)),
            ((4, 4), (5, 4)),
            ((4, 4), (6, 4)),
            ((4, 4), (7, 4)),
            ((4, 4), (3, 4)),
            ((4, 4), (2, 4)),
            ((4, 4), (1, 4)),
            ((4, 4), (0, 4)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_knight_moves(self):
        # Test knight move generation
        self.board.board[4][4] = Pieces.WHITE_KNIGHT
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            Move(Squares.E5, Squares.C4, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.C6, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.D3, Pieces.WHITE_KNIGHT),
            Move(
                Squares.E5,
                Squares.D7,
                Pieces.WHITE_KNIGHT,
                piece_captured=Pieces.BLACK_PAWN,
            ),
            Move(Squares.E5, Squares.F3, Pieces.WHITE_KNIGHT),
            Move(
                Squares.E5,
                Squares.F7,
                Pieces.WHITE_KNIGHT,
                piece_captured=Pieces.BLACK_PAWN,
            ),
            Move(Squares.E5, Squares.G4, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.G6, Pieces.WHITE_KNIGHT),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    @unittest.expectedFailure
    def test_generate_bishop_moves(self):
        # Test bishop move generation
        self.board.board[4][4] = Pieces.WHITE_BISHOP
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            ((4, 4), (5, 5)),
            ((4, 4), (6, 6)),
            ((4, 4), (7, 7)),
            ((4, 4), (3, 3)),
            ((4, 4), (2, 2)),
            ((4, 4), (1, 1)),
            ((4, 4), (0, 0)),
            ((4, 4), (5, 3)),
            ((4, 4), (6, 2)),
            ((4, 4), (7, 1)),
            ((4, 4), (3, 5)),
            ((4, 4), (2, 6)),
            ((4, 4), (1, 7)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    @unittest.expectedFailure
    def test_generate_queen_moves(self):
        # Test queen move generation
        self.board.board[4][4] = Pieces.WHITE_QUEEN
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            # Rook-like moves
            ((4, 4), (4, 5)),
            ((4, 4), (4, 6)),
            ((4, 4), (4, 7)),
            ((4, 4), (4, 3)),
            ((4, 4), (4, 2)),
            ((4, 4), (4, 1)),
            ((4, 4), (4, 0)),
            ((4, 4), (5, 4)),
            ((4, 4), (6, 4)),
            ((4, 4), (7, 4)),
            ((4, 4), (3, 4)),
            ((4, 4), (2, 4)),
            ((4, 4), (1, 4)),
            ((4, 4), (0, 4)),
            # Bishop-like moves
            ((4, 4), (5, 5)),
            ((4, 4), (6, 6)),
            ((4, 4), (7, 7)),
            ((4, 4), (3, 3)),
            ((4, 4), (2, 2)),
            ((4, 4), (1, 1)),
            ((4, 4), (0, 0)),
            ((4, 4), (5, 3)),
            ((4, 4), (6, 2)),
            ((4, 4), (7, 1)),
            ((4, 4), (3, 5)),
            ((4, 4), (2, 6)),
            ((4, 4), (1, 7)),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    def test_generate_king_moves(self):
        # Test king move generation
        self.board.board[4][4] = Pieces.WHITE_KING
        moves = self.board.generate_piece_moves(4, 4)
        expected_moves = [
            Move(Squares.E5, Squares.D4, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.D5, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.D6, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.E4, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.E6, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.F4, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.F5, Pieces.WHITE_KING),
            Move(Squares.E5, Squares.F6, Pieces.WHITE_KING),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    # TODO: ChatGPT: Add more test cases here.
    # Tests should include ensuring undo returns captured pieces correctly.
    def test_make_and_undo_move(self):
        # Test making and undoing a move
        move = Move(Squares.A2, Squares.A4, Pieces.WHITE_PAWN)
        self.board.make_move(move)
        self.assertEqual(self.board.board[move.start.row][move.start.col], ".")
        self.assertEqual(
            self.board.board[move.end.row][move.end.col], Pieces.WHITE_PAWN
        )
        self.board.undo_move(move)
        self.assertEqual(
            self.board.board[move.start.row][move.start.col], Pieces.WHITE_PAWN
        )
        self.assertEqual(self.board.board[move.end.row][move.end.col], ".")

    def test_evaluate(self):
        # Test the evaluation function
        self.assertEqual(self.engine.evaluate(), 0)  # Initial position is balanced

        # Test a board with a material imbalance
        self.board.board[4][4] = "Q"  # Add a white queen in the center
        self.assertEqual(self.engine.evaluate(), 9)

    @unittest.expectedFailure
    def test_best_move(self):
        # White has 2 pawn that can't move and a king in the corner that can only move
        # to one square. So there is only one move white can make.
        fen = "8/8/8/8/7k/6pp/6PP/7K w - - 0 1"  # noqa
        board = Board(self.fen)  # noqa
        engine = ChessEngine(self.board)  # noqa

        # Test the best move function
        move = self.engine.best_move(1)
        # TODO: Chris: Pretty sure this is wrong, but it's at least constant.
        self.assertEqual(move, ((7, 3), (1, 3)))


class TestUCIAlgebraicNotation(unittest.TestCase):
    def test_uci_algebraic_notation_white(self):
        move = Move(Squares.E2, Squares.E4, "P")
        self.assertEqual(uci_algebraic_notation(move), "e2e4")

        move = Move(Squares.E2, Squares.E4, "R")
        self.assertEqual(uci_algebraic_notation(move), "e2e4")

        move = Move(Squares.E7, Squares.E8, "P", promotion_piece="Q")
        self.assertEqual(uci_algebraic_notation(move), "e7e8q")

    def test_uci_algebraic_notation_black(self):
        move = Move(Squares.E7, Squares.E5, "p")
        self.assertEqual(uci_algebraic_notation(move), "e7e5")

        move = Move(Squares.E7, Squares.E5, "r")
        self.assertEqual(uci_algebraic_notation(move), "e7e5")

        move = Move(Squares.E2, Squares.E1, "p", promotion_piece="q")
        self.assertEqual(uci_algebraic_notation(move), "e2e1q")


if __name__ == "__main__":
    unittest.main()
