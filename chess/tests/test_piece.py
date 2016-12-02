import unittest

from unittest_expander import (
    expand,
    foreach,
)

from chess.board_loc import Location
from chess.exceptions import UserActionError
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

@expand
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
        self.assertRaises(UserActionError, white_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("a2"))  # move to the left
        self.assertRaises(UserActionError, white_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("b1"))  # white move down
        self.assertRaises(UserActionError, white_pawn.get_route, move)

        move = Move(src=Location("g1"), dst=Location("f1"))  # black move up
        self.assertRaises(UserActionError, black_pawn.get_route, move)

        move = Move(src=Location("b2"), dst=Location("b4"))  # white piece first move
        route = white_pawn.get_route(move)
        self.assertFalse(route.attack_required)
        self.assertTrue(route.attack_forbidden)

        # white piece not first two fields move
        move = Move(src=Location("b3"), dst=Location("b5"))
        self.assertRaises(UserActionError, white_pawn.get_route, move)

        # black piece first move
        move = Move(src=Location("b7"), dst=Location("b5"))
        route = black_pawn.get_route(move)
        self.assertFalse(route.attack_required)
        self.assertTrue(route.attack_forbidden)

        # black piece not first two fields move
        move = Move(src=Location("b6"), dst=Location("b4"))
        self.assertRaises(UserActionError, black_pawn.get_route, move)

        # white move attack
        move = Move(src=Location("b3"), dst=Location("a4"))
        route = white_pawn.get_route(move)
        self.assertTrue(route.attack_required)
        self.assertFalse(route.attack_forbidden)

    def test_bishop_move(self):
        bishop = self.piece_factory.create('B')

        move = Move(src=Location("b1"), dst=Location("a3"))
        self.assertRaises(UserActionError, bishop.get_route, move)

        move = Move(src=Location("b1"), dst=Location("c1"))
        self.assertRaises(UserActionError, bishop.get_route, move)

        move = Move(src=Location("b1"), dst=Location("b8"))
        self.assertRaises(UserActionError, bishop.get_route, move)

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
        self.assertRaises(UserActionError, queen.get_route, move)

    @foreach([
        ('d4', 'e6'),
        ('d4', 'c6'),
        ('d4', 'b5'),
        ('d4', 'b3'),
        ('d4', 'c2'),
        ('d4', 'e2'),
        ('d4', 'f3'),
        ('d4', 'f5'),
    ])
    def test_knight_correct_move(self, src, dst):
        knight = self.piece_factory.create('N')
        move = Move(src=Location(src), dst=Location(dst))
        knight.get_route(move)

    @foreach([
        ('d1', 'e6'),
        ('d2', 'c6'),
        ('d3', 'b5'),
        ('d5', 'b3'),
        ('c4', 'c2'),
        ('f4', 'e3'),
        ('g4', 'f7'),
        ('h3', 'f5'),
    ])
    def test_knight_illegal_move(self, src, dst):
        knight = self.piece_factory.create('N')
        move = Move(src=Location(src), dst=Location(dst))
        self.assertRaises(UserActionError, knight.get_route, move)

    @foreach([
        ('d4', 'd6'),
        ('d4', 'c4'),
        ('d1', 'd8'),
        ('a7', 'h7'),
    ])
    def test_rook_correct_move(self, src, dst):
        rook = self.piece_factory.create('R')
        move = Move(src=Location(src), dst=Location(dst))
        rook.get_route(move)

    @foreach([
        ('d4', 'c6'),
        ('d4', 'c6'),
        ('a1', 'h8'),
    ])
    def test_rook_illegal_move(self, src, dst):
        rook = self.piece_factory.create('R')
        move = Move(src=Location(src), dst=Location(dst))
        self.assertRaises(UserActionError, rook.get_route, move)

    @foreach([
        ('d4', 'c5'),
        ('d4', 'd5'),
        ('d4', 'e5'),
        ('d4', 'e4'),
        ('d4', 'e3'),
        ('d4', 'd3'),
        ('d4', 'c3'),
        ('d4', 'c4'),
    ])
    def test_king_correct_move(self, src, dst):
        king = self.piece_factory.create('K')
        move = Move(src=Location(src), dst=Location(dst))
        king.get_route(move)

    @foreach([
        ('d4', 'a8'),
        ('d4', 'd6'),
        ('d4', 'f6'),
        ('d4', 'd2'),
        ('d4', 'b4'),
        ('d4', 'g1'),
        ('d4', 'a5'),
        ('d4', 'h8'),
    ])
    def test_king_illegal_move(self, src, dst):
        king = self.piece_factory.create('K')
        move = Move(src=Location(src), dst=Location(dst))
        self.assertRaises(UserActionError, king.get_route, move)

    def test_rook_attacked_locations(self):
        rook = self.piece_factory.create('R')

        attacked_locations = rook.get_attacked_locations(Location('a1'))
        valid_attacked_locations = [
            Location('a2'),
            Location('a3'),
            Location('a4'),
            Location('a5'),
            Location('a6'),
            Location('a7'),
            Location('a8'),
            Location('b1'),
            Location('c1'),
            Location('d1'),
            Location('e1'),
            Location('f1'),
            Location('g1'),
            Location('h1'),
        ]
        self.assertItemsEqual(attacked_locations, valid_attacked_locations)

        attacked_locations = rook.get_attacked_locations(Location('g4'))
        valid_attacked_locations = [
            Location('g1'),
            Location('g2'),
            Location('g3'),
            Location('g5'),
            Location('g6'),
            Location('g7'),
            Location('g8'),
            Location('a4'),
            Location('b4'),
            Location('c4'),
            Location('d4'),
            Location('e4'),
            Location('f4'),
            Location('h4'),
        ]
        self.assertItemsEqual(attacked_locations, valid_attacked_locations)

    def test_bishop_attacked_locations(self):
        bishop = self.piece_factory.create('B')

        attacked_locations = bishop.get_attacked_locations(Location('C2'))
        valid_attacked_locations = [
            Location('b1'),
            Location('d3'),
            Location('e4'),
            Location('f5'),
            Location('g6'),
            Location('h7'),
            Location('b3'),
            Location('a4'),
            Location('d1'),
        ]

        self.assertItemsEqual(attacked_locations, valid_attacked_locations)

        attacked_locations = bishop.get_attacked_locations(Location('a1'))
        valid_attacked_locations = [
            Location('b2'),
            Location('c3'),
            Location('d4'),
            Location('e5'),
            Location('f6'),
            Location('g7'),
            Location('h8'),
        ]

        self.assertItemsEqual(attacked_locations, valid_attacked_locations)

    def test_queen_attacked_locations(self):
        pass