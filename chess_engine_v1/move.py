class Move:
    def __init__(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        piece_moved: str,
        piece_captured: str = " ",
        promotion_piece: str | None = None,
    ):
        self.start: tuple[int, int] = start
        self.end: tuple[int, int] = end
        self.piece_moved: str = piece_moved
        self.piece_captured: str = piece_captured
        self.promotion_piece: str | None = promotion_piece

    def __str__(self) -> str:
        if self.promotion_piece:
            return f"{self.piece_moved} from {self.start} to {self.end}, capturing {self.piece_captured}, promoting to {self.promotion_piece}"  # noqa
        else:
            return f"{self.piece_moved} from {self.start} to {self.end}, capturing {self.piece_captured}"  # noqa

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
