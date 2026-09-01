import unittest

from chessengine.board import Board, Move, sq
from chessengine.engine import evaluate, search_best_move


class TestBoard(unittest.TestCase):
    def test_start_moves(self):
        b = Board()
        moves = b.generate_legal_moves()
        self.assertEqual(len(moves), 20)

    def test_make_move_e2e4(self):
        b = Board()
        b.make_move(Move(sq(4, 1), sq(4, 3)))
        self.assertEqual(b.piece_at(sq(4, 3)), "P")
        self.assertIsNone(b.piece_at(sq(4, 1)))
        self.assertFalse(b.white_to_move)


class TestSearch(unittest.TestCase):
    def test_captures_hanging_queen(self):
        fen = "4k3/8/8/3q4/8/2N5/8/4K3 w - - 0 1"
        b = Board(fen)
        move, score = search_best_move(b, depth=2)
        self.assertIsNotNone(move)
        assert move is not None
        self.assertEqual(move.uci(), "c3d5")
        self.assertGreater(evaluate(b), -1000)


if __name__ == "__main__":
    unittest.main()
