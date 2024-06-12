import unittest
from unittest.mock import patch
from io import StringIO
from chess_engine import UCIInterface

class TestUCIInterface(unittest.TestCase):

    @patch('sys.stdin', StringIO('uci\nisready\nposition fen rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1\ngo depth 1\nd\nquit\n'))
    @patch('sys.stdout', new_callable=StringIO)
    def test_uci_commands(self, mock_stdout):
        uci_interface = UCIInterface()
        uci_interface.run()

        output = mock_stdout.getvalue().strip().split('\n')
        expected_output = [
            "id name SimpleChessEngine",
            "id author YourName",
            "uciok",
            "readyok",
            "bestmove e2e3"  # Note: The exact move may vary depending on implementation
        ]

        # Check that the UCI responses are as expected
        self.assertEqual(output[:5], expected_output[:5])
        #self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
