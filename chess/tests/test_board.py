import unittest

from chess.board_loc import Board


class TestBoard(unittest.TestCase):

    def test_setup_and_getitem(self):
        board = Board()
        board.setup()
        self.assertEqual(board['a1'].get_symbol(), 'R')
        self.assertEqual(board['e2'].get_symbol(), 'P')
        self.assertIsNone(board['c3'])
        self.assertIsNone(board['c3'])
        self.assertEqual(board['d8'].get_symbol(), 'q')
        self.assertEqual(board['h8'].get_symbol(), 'r')

    def test_setitem(self):
        board = Board()
        board.setup()
        TODO
