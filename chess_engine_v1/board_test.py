import unittest

import fen
from board import Board, Pieces
from move import Move
from square import Squares


class TestBoard(unittest.TestCase):
    def test_parse_fen(self) -> None:
        board = Board(fen.STARTING_GAME_FEN)
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
        self.assertEqual(board.board, expected_board)

    # TODO: ChatGPT: Add non-new game FEN tests.

    # TODO: ChatGPT: Add tests for:
    # -Different positions
    # -Black pieces
    # -En-passant pawn captures
    # -Pawn promotions
    # -Where some squares are blocked

    def test_generate_pawn_moves(self) -> None:
        # Test pawn move generation
        board = Board()
        board.board[1][0] = Pieces.WHITE_PAWN
        moves = board.generate_piece_moves(1, 0)
        expected_moves = [
            Move(Squares.A2, Squares.A3, Pieces.WHITE_PAWN),
            Move(Squares.A2, Squares.A4, Pieces.WHITE_PAWN),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    @unittest.expectedFailure
    def test_generate_rook_moves(self) -> None:
        board = Board()
        board.board[4][4] = Pieces.WHITE_ROOK
        moves = board.generate_piece_moves(4, 4)
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

    def test_generate_knight_moves(self) -> None:
        board = Board()
        board.board[4][4] = Pieces.WHITE_KNIGHT
        moves = board.generate_piece_moves(4, 4)
        expected_moves = [
            Move(Squares.E5, Squares.C4, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.C6, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.D3, Pieces.WHITE_KNIGHT),
            Move(
                Squares.E5,
                Squares.D7,
                Pieces.WHITE_KNIGHT,
            ),
            Move(Squares.E5, Squares.F3, Pieces.WHITE_KNIGHT),
            Move(
                Squares.E5,
                Squares.F7,
                Pieces.WHITE_KNIGHT,
            ),
            Move(Squares.E5, Squares.G4, Pieces.WHITE_KNIGHT),
            Move(Squares.E5, Squares.G6, Pieces.WHITE_KNIGHT),
        ]
        self.assertSetEqual(set(moves), set(expected_moves))

    @unittest.expectedFailure
    def test_generate_bishop_moves(self) -> None:
        board = Board()
        board.board[4][4] = Pieces.WHITE_BISHOP
        moves = board.generate_piece_moves(4, 4)
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
    def test_generate_queen_moves(self) -> None:
        board = Board()
        board.board[4][4] = Pieces.WHITE_QUEEN
        moves = board.generate_piece_moves(4, 4)
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

    def test_generate_king_moves(self) -> None:
        board = Board()
        board.board[4][4] = Pieces.WHITE_KING
        moves = board.generate_piece_moves(4, 4)
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
    def test_make_and_undo_move(self) -> None:
        board = Board()
        board.board[0][1] = Pieces.WHITE_PAWN
        move = Move(Squares.A2, Squares.A4, Pieces.WHITE_PAWN)
        board.make_move(move)
        self.assertEqual(board.board[move.start.row][move.start.col], ".")
        self.assertEqual(board.board[move.end.row][move.end.col], Pieces.WHITE_PAWN)
        board.undo_move(move)
        self.assertEqual(board.board[move.start.row][move.start.col], Pieces.WHITE_PAWN)
        self.assertEqual(board.board[move.end.row][move.end.col], ".")
