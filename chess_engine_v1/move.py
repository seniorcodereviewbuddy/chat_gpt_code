from square import Square

BOARD_SIZE = 8


class Move:
    def __init__(
        self,
        start: Square,
        end: Square,
        piece_moved: str,
        piece_captured: str | None = None,
        promotion_piece: str | None = None,
    ):
        self.start = start
        self.end = end
        self.piece_moved = piece_moved
        self.piece_captured = piece_captured
        self.promotion_piece = promotion_piece

    def __str__(self) -> str:
        val = f"{self.piece_moved} from {self.start} to {self.end}"

        if self.piece_captured:
            val += f", capturing {self.piece_captured}"

        if self.promotion_piece:
            val += f", promoting to {self.promotion_piece}"

        return val

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Move):
            return NotImplemented
        return (
            self.start == other.start
            and self.end == other.end
            and self.piece_moved == other.piece_moved
            and self.piece_captured == other.piece_captured
            and self.promotion_piece == other.promotion_piece
        )

    def __hash__(self) -> int:
        return hash(
            (
                self.start,
                self.end,
                self.piece_moved,
                self.piece_captured,
                self.promotion_piece,
            )
        )
