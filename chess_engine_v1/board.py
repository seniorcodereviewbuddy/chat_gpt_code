import enum

import fen
from move import Move
from square import Squares


class Player(enum.Enum):
    WHITE = 1
    BLACK = 2


class Pieces(enum.StrEnum):
    WHITE_KING = "K"
    WHITE_QUEEN = "Q"
    WHITE_BISHOP = "B"
    WHITE_KNIGHT = "N"
    WHITE_ROOK = "R"
    WHITE_PAWN = "P"
    BLACK_KING = "k"
    BLACK_QUEEN = "q"
    BLACK_BISHOP = "b"
    BLACK_KNIGHT = "n"
    BLACK_ROOK = "r"
    BLACK_PAWN = "p"


DIAGONAL_DIRECTIONS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
VERTICAL_AND_HORIZONTAL_DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
ALL_DIRECTIONS = VERTICAL_AND_HORIZONTAL_DIRECTIONS + DIAGONAL_DIRECTIONS
KNIGHT_MOVES = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]

BOARD_SIZE = 8


class Board:
    def __init__(self, fen_str: str | None = None):
        # Initialize the board using FEN notation if present.
        # Otherwise default to an empty board.
        if fen_str:
            fen_record = fen.FENRecord(fen_str)
            self.board = fen_record.board()
        else:
            self.board = [["."] * int(BOARD_SIZE) for _ in range(BOARD_SIZE)]
        self.turn = Player.WHITE

    def display(self) -> None:
        # Print the board state
        # Print the board reversed as row 1 is stored first in the array, but we want
        # to print row 8 at the top first.
        for row in reversed(self.board):
            print(" ".join(row))
        print()

    def print_legal_moves(self) -> None:
        legal_moves = self.generate_moves()
        legal_moves_as_algo = [
            move.start.algebraic + move.end.algebraic for move in legal_moves
        ]
        print("Legal moves:\n" + " ".join(legal_moves_as_algo))

    def _piece_owned_by_current_player(self, piece: str) -> bool:
        return piece.isupper() if self.turn == Player.WHITE else piece.islower()

    def _piece_capturable_by_current_player(self, piece: str) -> bool:
        return not self._piece_owned_by_current_player(piece)

    def _create_move(
        self, initial_row: int, initial_col: int, new_row: int, new_col: int
    ) -> Move:
        initial_square = Squares.square_from_row_col(initial_row, initial_col)
        new_square = Squares.square_from_row_col(new_row, new_col)
        moving_piece = self.board[initial_row][initial_col]
        captured_piece = (
            None
            if self.board[new_row][new_col] == "."
            else self.board[new_row][new_col]
        )
        return Move(initial_square, new_square, moving_piece, captured_piece)

    def generate_moves(self) -> list[Move]:
        # Generate all legal moves for the current player
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if self._piece_owned_by_current_player(piece):
                    moves.extend(self.generate_piece_moves(r, c))
        return moves

    def generate_piece_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal moves for a specific piece

        # TODO: ChatGPT: Remove moves that expose the king to capture.
        piece = self.board[r][c]
        if piece.upper() == Pieces.WHITE_PAWN:
            return self.generate_pawn_moves(r, c)
        elif piece.upper() == Pieces.WHITE_ROOK:
            return self.generate_rook_moves(r, c)
        elif piece.upper() == Pieces.WHITE_KNIGHT:
            return self.generate_knight_moves(r, c)
        elif piece.upper() == Pieces.WHITE_BISHOP:
            return self.generate_bishop_moves(r, c)
        elif piece.upper() == Pieces.WHITE_QUEEN:
            return self.generate_queen_moves(r, c)
        elif piece.upper() == Pieces.WHITE_KING:
            return self.generate_king_moves(r, c)

        raise Exception(f"Trying to generate moves for an unknown piece, {piece}")

    def generate_pawn_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal pawn moves
        moves = []
        direction = 1 if self.turn == Player.WHITE else -1
        start_row = 1 if self.turn == Player.WHITE else 6

        # Single square move
        if self.board[r + direction][c] == ".":
            moves.append(self._create_move(r, c, r + direction, c))
            # Double square move
            if r == start_row and self.board[r + 2 * direction][c] == ".":
                moves.append(self._create_move(r, c, r + 2 * direction, c))

        # Captures
        # TODO: ChatGPT: Handle en-passant captures.
        for dc in [-1, 1]:
            new_r = r + direction
            new_c = c + dc
            if (
                0 <= new_c < BOARD_SIZE
                and self.board[new_r][new_c] != "."
                and self._piece_capturable_by_current_player(self.board[new_r][new_c])
            ):
                moves.append(self._create_move(r, c, new_r, new_c))

        # TODO: ChatGPT: Handle promotion when the pawn reaches the final row.

        return moves

    def generate_rook_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal rook moves
        return self.generate_sliding_moves(r, c, VERTICAL_AND_HORIZONTAL_DIRECTIONS)

    def generate_bishop_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal bishop moves
        return self.generate_sliding_moves(r, c, DIAGONAL_DIRECTIONS)

    def generate_queen_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal queen moves
        return self.generate_sliding_moves(r, c, ALL_DIRECTIONS)

    def _on_board(self, r: int, c: int) -> bool:
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def generate_sliding_moves(
        self, r: int, c: int, directions: list[tuple[int, int]]
    ) -> list[Move]:
        # Generate sliding moves for rooks, bishops, and queens.
        piece = self.board[r][c]  # noqa
        moves = []
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while self._on_board(nr, nc):
                if self.board[nr][
                    nc
                ] == "." or self._piece_capturable_by_current_player(
                    self.board[nr][nc]
                ):
                    moves.append(self._create_move(r, c, nr, nc))
                    break
                nr += dr
                nc += dc
        return moves

    def generate_knight_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal knight moves
        moves = []
        for dr, dc in KNIGHT_MOVES:
            nr, nc = r + dr, c + dc
            if self._on_board(nr, nc):
                if self.board[nr][
                    nc
                ] == "." or self._piece_capturable_by_current_player(
                    self.board[nr][nc]
                ):
                    moves.append(self._create_move(r, c, nr, nc))
        return moves

    def generate_king_moves(self, r: int, c: int) -> list[Move]:
        # Generate legal king moves
        moves = []
        for dr, dc in ALL_DIRECTIONS:
            nr, nc = r + dr, c + dc
            if self._on_board(nr, nc):
                if self.board[nr][nc] == "." or self._piece_owned_by_current_player(
                    self.board[nr][nc]
                ):
                    moves.append(self._create_move(r, c, nr, nc))
        return moves

    def make_move(self, move: Move) -> None:
        # Make a move on the board
        self.board[move.end.row][move.end.col] = (
            move.promotion_piece if move.promotion_piece else move.piece_moved
        )
        self.board[move.start.row][move.start.col] = "."

    def undo_move(self, move: Move) -> None:
        # Undo a move on the board
        self.board[move.start.row][move.start.col] = move.piece_moved
        self.board[move.end.row][move.end.col] = (
            move.piece_captured if move.piece_captured else "."
        )
