import unittest
from collections import namedtuple

from chess.board_loc import Location
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


class Move(object):

    def __init__(self, src, dst):
        self.src = src
        self.dst = dst

    def get_vector(self):
        return self.src.get_vector(self.dst)

    def get_path(self):
        return self.src.get_path(self.dst)


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

    def test_pawn_first_move(self):
        white_pawn = self.piece_factory.create('P')
        black_pawn = self.piece_factory.create('p')

        white_first_move = Move(src=Location("b2"), dst=Location("b4"))
        black_first_move = Move(src=Location("g7"), dst=Location("g5"))

        self.assertTrue(white_pawn._first_move(white_first_move))
        self.assertFalse(white_pawn._first_move(black_first_move))

        self.assertTrue(black_pawn._first_move(black_first_move))
        self.assertFalse(black_pawn._first_move(white_first_move))

    def test_pawn_move(self):
        white_pawn = self.piece_factory.create('P')
        black_pawn = self.piece_factory.create('p')

        move = Move(src=Location("b2"), dst=Location("c2"))  # move to the right
        self.assertRaises(IllegalMoveError, white_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("a2"))  # move to the left
        self.assertRaises(IllegalMoveError, white_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("b1"))  # white move down
        self.assertRaises(IllegalMoveError, white_pawn.get_route, move)

        move = Move(src=Location("g1"), dst=Location("f1"))  # black move up
        self.assertRaises(IllegalMoveError, black_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("b4"))  # white piece first move
        route = white_pawn.get_route(move)
        self.assertFalse(route.must_be_attack)
        self.assertTrue(route.must_not_be_attack)

        # white piece not first two fields move
        move = Move(src=Location("b3"), dst=Location("b5"))
        self.assertRaises(IllegalMoveError, white_pawn.get_route, move)

        # black piece first move
        move = Move(src=Location("b7"), dst=Location("b5"))
        route = black_pawn.get_route(move)
        self.assertFalse(route.must_be_attack)
        self.assertTrue(route.must_not_be_attack)

        # black piece not first two fields move
        move = Move(src=Location("b6"), dst=Location("b4"))
        self.assertRaises(IllegalMoveError, black_pawn.get_route, move)

        # white move attack
        move = Move(src=Location("b3"), dst=Location("a4"))
        route = white_pawn.get_route(move)
        self.assertTrue(route.must_be_attack)
        self.assertFalse(route.must_not_be_attack)

    def test_bishop_move(self):
        bishop = self.piece_factory.create('B')

        move = Move(src=Location("b1"), dst=Location("a3"))
        self.assertRaises(IllegalMoveError, bishop.get_route, move)

        move = Move(src=Location("b1"), dst=Location("c1"))
        self.assertRaises(IllegalMoveError, bishop.get_route, move)

        move = Move(src=Location("b1"), dst=Location("b8"))
        self.assertRaises(IllegalMoveError, bishop.get_route, move)

        moves = [
            Move(src=Location("b1"), dst=Location("a2")),
            Move(src=Location("a2"), dst=Location("e6")),
            Move(src=Location("e6"), dst=Location("g4")),
            Move(src=Location("g4"), dst=Location("h5")),
            Move(src=Location("h5"), dst=Location("e8"))
        ]
        for move in moves:
            bishop.get_route(move)

    def test_queen_move(self):
        queen = self.piece_factory.create('Q')

        moves = [
            Move(src=Location("b1"), dst=Location("a1")),
            Move(src=Location("b1"), dst=Location("b8")),
            Move(src=Location("b1"), dst=Location("g6")),
        ]
        for move in moves:
            queen.get_route(move)

        move = Move(src=Location("b1"), dst=Location("h3"))
        self.assertRaises(IllegalMoveError, queen.get_route, move)
