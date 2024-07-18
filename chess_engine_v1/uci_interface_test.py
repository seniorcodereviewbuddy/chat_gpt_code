import unittest
from unittest.mock import patch
from io import StringIO
from chess_engine import UCIInterface


class TestUCIInterface(unittest.TestCase):
    @patch(
        "sys.stdin",
        StringIO(
            "uci\nisready\nposition fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1\ngo depth 1\nd\nquit\n"
        ),
    )
    @patch("sys.stdout", new_callable=StringIO)
    def test_uci_commands(self, mock_stdout):
        uci_interface = UCIInterface()
        uci_interface.run()

        output = mock_stdout.getvalue().strip().split("\n")
        expected_output = [
            "id name SimpleChessEngine",
            "id author SCRB",
            "uciok",
            "readyok",
            "bestmove [a-h][1-8][a-h][1-8]",  # Note: The exact move may vary depending on implementation
        ]

        # TODO: look at all output, not just the first 5 lines.
        for i in range(5):
            self.assertRegex(output[i], expected_output[i])

    # TODO: ChatGPT: Add test for self_play file.


if __name__ == "__main__":
    unittest.main()
