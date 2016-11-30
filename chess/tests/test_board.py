import unittest

from chess.board_loc import Board


class TestBoard(unittest.TestCase):

    def test_setup_and_getitem(self):
        board = Board()
        board.setup()
        self.assertEqual(board['a1'].symbol, 'R')
        self.assertEqual(board['a1'].is_white, True)
        self.assertEqual(board['e2'].symbol, 'P')
        self.assertEqual(board['e2'].is_white, True)
        self.assertIsNone(board['c3'])
        self.assertIsNone(board['c3'])
        self.assertEqual(board['d8'].symbol, 'Q')
        self.assertEqual(board['d8'].is_white, False)
        self.assertEqual(board['h8'].symbol, 'R')
        self.assertEqual(board['h8'].is_white, False)

    def test_setitem(self):
        board = Board()
        board.setup()
        TODO
