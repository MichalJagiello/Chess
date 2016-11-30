import unittest

from chess.exceptions import IllegalMoveError
from chess.piece import (
    PieceFactory,
    Pawn,
    King,
    Knight,
    Queen,
    Rook,
    Bishop,
)


class PieceTestCase(unittest.TestCase):

    def setUp(self):
        self.piece_factory = PieceFactory()

    def test_piece_factory(self):
        symbol = 'P'
        white_pawn = self.piece_factory.create(symbol)
        self.assertIsInstance(white_pawn, Pawn)
        self.assertTrue(white_pawn.is_white)
        self.assertEqual(white_pawn.get_symbol(), symbol)

        symbol = 'p'
        black_pawn = self.piece_factory.create(symbol)
        self.assertIsInstance(black_pawn, Pawn)
        self.assertFalse(black_pawn.is_white)
        self.assertEqual(black_pawn.get_symbol(), symbol)

        symbol = 'N'
        white_knight = self.piece_factory.create(symbol)
        self.assertIsInstance(white_knight, Knight)
        self.assertTrue(white_knight.is_white)
        self.assertEqual(white_knight.get_symbol(), symbol)

        symbol = 'n'
        black_knight = self.piece_factory.create(symbol)
        self.assertIsInstance(black_knight, Knight)
        self.assertFalse(black_knight.is_white)
        self.assertEqual(black_knight.get_symbol(), symbol)

        symbol = 'B'
        white_bishop = self.piece_factory.create(symbol)
        self.assertIsInstance(white_bishop, Bishop)
        self.assertTrue(white_bishop.is_white)
        self.assertEqual(white_bishop.get_symbol(), symbol)

        symbol = 'b'
        black_bishop = self.piece_factory.create(symbol)
        self.assertIsInstance(black_bishop, Bishop)
        self.assertFalse(black_bishop.is_white)
        self.assertEqual(black_bishop.get_symbol(), symbol)

        symbol = 'R'
        white_rook = self.piece_factory.create(symbol)
        self.assertIsInstance(white_rook, Rook)
        self.assertTrue(white_rook.is_white)
        self.assertEqual(white_rook.get_symbol(), symbol)

        symbol = 'r'
        black_rook = self.piece_factory.create(symbol)
        self.assertIsInstance(black_rook, Rook)
        self.assertFalse(black_rook.is_white)
        self.assertEqual(black_rook.get_symbol(), symbol)

        symbol = 'Q'
        white_queen = self.piece_factory.create(symbol)
        self.assertIsInstance(white_queen, Queen)
        self.assertTrue(white_queen.is_white)
        self.assertEqual(white_queen.get_symbol(), symbol)

        symbol = 'q'
        black_queen = self.piece_factory.create(symbol)
        self.assertIsInstance(black_queen, Queen)
        self.assertFalse(black_queen.is_white)
        self.assertEqual(black_queen.get_symbol(), symbol)

        symbol = 'K'
        white_king = self.piece_factory.create(symbol)
        self.assertIsInstance(white_king, King)
        self.assertTrue(white_king.is_white)
        self.assertEqual(white_king.get_symbol(), symbol)

        symbol = 'k'
        black_king = self.piece_factory.create(symbol)
        self.assertIsInstance(black_king, King)
        self.assertFalse(black_king.is_white)
        self.assertEqual(black_king.get_symbol(), symbol)

    def test_pawn_move(self):
        white_pawn = self.piece_factory.create('P')
