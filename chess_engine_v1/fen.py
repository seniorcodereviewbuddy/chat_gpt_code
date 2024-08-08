import board

STARTING_GAME_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


class FENRecord:
    # TODO: Add tests for FENRecord.

    """You can learn more about the FEN Record format at https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation"""

    def __init__(self, fen_str: str):
        fen_parts = fen_str.split(" ")
        self.board_str = fen_parts[0]

        # TODO: ChatGPT: Handle rest of FEN string.

    def board(self) -> list[list[str]]:
        def valid_board_character(character: str) -> bool:
            return character in [
                "k",
                "K",
                "Q",
                "q",
                "B",
                "b",
                "N",
                "n",
                "R",
                "r",
                "P",
                "p",
            ]

        fen_board = []
        rows = self.board_str.split("/")
        # Store the rows in reversed order because FEN start with row 8 and works down
        # to row 1.
        for row in reversed(rows):
            board_row = []
            for char in row:
                if char.isdigit():
                    board_row.extend(["."] * int(char))
                else:
                    if valid_board_character:  # type: ignore
                        board_row.append(char)
                    else:
                        raise Exception(f"Invalid chracter in FEN board, {char}")

            if len(board_row) != board.BOARD_SIZE:
                raise Exception(
                    f"FEN record error, found row of size {len(board_row)}, "
                    f"expecting {board.BOARD_SIZE}"
                )
            fen_board.append(board_row)
        return fen_board
