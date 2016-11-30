import unittest

from unittest_expander import (
    expand,
    foreach,
    param,
)

from chess.board_loc import (
    Board,
    Location,
)
from chess.piece import (
    Piece,
    PieceFactory,
)


@expand
class TestBoard(unittest.TestCase):

    setup_and_getitem_piece_test_data = [
        # (<location label>, <piece symbol>)
        ('a1', 'R'),
        ('b1', 'N'),
        ('h1', 'R'),
        ('b2', 'P'),
        ('e2', 'P'),
        ('a2', 'p'),
        ('e7', 'p'),
        ('a8', 'r'),
        ('d8', 'q'),
        ('f8', 'b'),
        ('h8', 'r'),
    ]

    getitem_none_test_data = [
        # (<location label>,)
        ('a3',),
        ('a6',),
        ('d5',),
        ('f4',),
        ('h3',),
        ('h6',),
    ]

    setup_and_delitem_test_data = getitem_none_test_data + [
        (loc_label,) for loc_label, _ in setup_and_getitem_piece_test_data]

    setitem_test_data = getitem_piece_test_data + [
        ('a1', 'K'),
        ('b1', 'n'),
        ('h1', 'Q'),
        ('b2', 'p'),
        ('e2', 'b'),
        ('a2', 'N'),
        ('e7', 'P'),
        ('a8', 'Q'),
        ('d8', 'R'),
        ('f8', 'B'),
        ('h8', 'k'),
    ]

    setup_and_pop_test_data = getitem_none_test_data + setup_and_getitem_piece_test_data


    def setUp(self):
        self.board = Board()
        self.board.setup()

    @foreach(setup_and_getitem_piece_test_data)
    def test_setup_and_getitem_piece(self, loc_label, expected_symbol):
        loc = Location(loc_label)
        value = self.board[loc]
        self.assertIsInstance(value, Piece)
        self.assertEqual(value.get_symbol(), expected_symbol)

    @foreach(getitem_none_test_data)
    def test_getitem_none(self, loc_label):
        loc = Location(loc_label)
        value = self.board[loc]
        self.assertIsNone(value)

    @foreach(setitem_test_data)
    def test_setitem(self, loc_label, symbol):
        piece_factory = PieceFactory()
        fresh_board = Board()
        loc = Location(loc_label)
        piece = piece_factory.create(symbol)
        fresh_board[loc] = piece
        value = fresh_board[loc]
        self.assertIs(value, piece)

    @foreach(setup_and_delitem_test_data)
    def test_setup_and_delitem(self, loc_label):
        loc = Location(loc_label)
        del self.board[loc]
        value_after = self.board[loc]
        self.assertIsNone(value_after)

    @foreach(setup_and_pop_test_data)
    def test_setup_and_pop(self, loc_label, expected_symbol=None):
        loc = Location(loc_label)
        value = self.board.pop(loc)
        value_after = self.board[loc]
        if value is None:
            self.assertIsNone(expected_symbol)
        else:
            self.assertIsInstance(value, Piece)
            self.assertEqual(value.get_symbol(), expected_symbol)
        self.assertIsNone(value_after)
