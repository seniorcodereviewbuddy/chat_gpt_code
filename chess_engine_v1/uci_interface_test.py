import unittest
from io import StringIO
from unittest.mock import patch

import fen
from chess_engine import UCIInterface


class TestUCIInterface(unittest.TestCase):
    @patch(
        "sys.stdin",
        StringIO(
            "\n".join(
                [
                    "uci",
                    "isready",
                    f"position fen {fen.STARTING_GAME_FEN}",
                    "go depth 1",
                    "d",
                    "quit",
                ]
            )
        ),
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_uci_commands(self, mock_stdout: StringIO) -> None:
        uci_interface = UCIInterface()
        uci_interface.run()

        output = mock_stdout.getvalue().strip().split("\n")
        expected_output = [
            "id name SimpleChessEngine",
            "id author SCRB",
            "uciok",
            "readyok",
            # Note: The exact move may vary depending on implementation.
            "bestmove [a-h][1-8][a-h][1-8]",
        ]

        # TODO: look at all output, not just the first 5 lines.
        for i in range(5):
            self.assertRegex(output[i], expected_output[i])

    # TODO: ChatGPT: Add test for self_play file.


if __name__ == "__main__":
    unittest.main()
