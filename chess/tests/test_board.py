import collections
import unittest

from unittest_expander import (
    expand,
    foreach,
)

from chess.board_loc import (
    Board,
    Location,
)
from chess.exceptions import (
    IllegalMoveError,
    InvalidLocationLabelError,
)
from chess.piece import (
    Piece,
    PieceFactory,
)


@expand
class TestBoard(unittest.TestCase):

    getitem_piece_cases = [
        # (<location label>, <piece symbol>)
        ('a1', 'R'),
        ('b1', 'N'),
        ('h1', 'R'),
        ('b2', 'P'),
        ('e2', 'P'),
        ('a2', 'P'),
        ('e7', 'p'),
        ('a8', 'r'),
        ('d8', 'q'),
        ('f8', 'b'),
        ('h8', 'r'),
    ]

    getitem_none_cases = [
        # (<location label>,)
        ('a3',),
        ('a6',),
        ('d5',),
        ('f4',),
        ('h3',),
        ('h6',),
    ]

    setitem_cases = getitem_piece_cases + [
        # (<location label>, <piece symbol>)
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

    no_pieces_cases = delitem_cases = getitem_none_cases + [
        (loc_label,) for loc_label, _ in getitem_piece_cases]

    pop_piece_cases = getitem_none_cases + getitem_piece_cases


    def setUp(self):
        self.board = Board()
        self.board.setup()

    @foreach(no_pieces_cases)
    def test_init(self, loc_label):
        fresh_board = Board()
        loc = Location(loc_label)
        value = fresh_board[loc]
        self.assertIsNone(value)

    @foreach(getitem_piece_cases)
    def test_getitem_piece(self, loc_label, expected_symbol):
        loc = Location(loc_label)
        value = self.board[loc]
        self.assertIsInstance(value, Piece)
        self.assertEqual(value.get_symbol(), expected_symbol)

    @foreach(getitem_none_cases)
    def test_getitem_none(self, loc_label):
        loc = Location(loc_label)
        value = self.board[loc]
        self.assertIsNone(value)

    @foreach(setitem_cases)
    def test_setitem(self, loc_label, symbol):
        piece_factory = PieceFactory()
        loc = Location(loc_label)
        piece = piece_factory.create(symbol)
        self.board[loc] = piece
        value = self.board[loc]
        self.assertIs(value, piece)

    @foreach(delitem_cases)
    def test_delitem(self, loc_label):
        loc = Location(loc_label)
        del self.board[loc]
        value_after = self.board[loc]
        self.assertIsNone(value_after)

    @foreach(pop_piece_cases)
    def test_pop_piece(self, loc_label, expected_symbol=None):
        loc = Location(loc_label)
        value = self.board.pop_piece(loc)
        value_after = self.board[loc]
        if value is None:
            self.assertIsNone(expected_symbol)
        else:
            self.assertIsInstance(value, Piece)
            self.assertEqual(value.get_symbol(), expected_symbol)
        self.assertIsNone(value_after)

    def test_iter_rows(self):
        row_iterator = self.board.iter_rows()
        rows = list(row_iterator)
        rows_of_symbols = [
            ''.join(
                ' ' if piece is None else piece.get_symbol()
                for piece in row
            ) for row in rows]
        self.assertIsInstance(row_iterator, collections.Iterator)
        self.assertTrue(all(isinstance(row, tuple)
                            for row in rows))
        self.assertEqual(rows_of_symbols, [
            'rnbqkbnr',
            'pppppppp',
            '        ',
            '        ',
            '        ',
            '        ',
            'PPPPPPPP',
            'RNBQKBNR',
        ])

    def test_iter_x_labels(self):
        func = Board.iter_x_labels
        iterator = func()
        x_labels = ''.join(iterator)
        self.assertIs(self.board.iter_x_labels, func)
        self.assertIsInstance(iterator, collections.Iterator)
        self.assertEqual(x_labels, 'abcdefgh')

    def test_iter_y_labels(self):
        func = Board.iter_y_labels
        iterator = func()
        y_labels = ''.join(iterator)
        self.assertIs(self.board.iter_y_labels, func)
        self.assertIsInstance(iterator, collections.Iterator)
        self.assertEqual(y_labels, '87654321')


@expand
class TestLocation(unittest.TestCase):

    init_and_basics_cases = [
        # location label
        'a1',
        'b1',
        'h1',
        'b2',
        'e2',
        'A2',
        'E7',
        'A8',
        'D8',
        'F8',
        'H8',
    ]

    init_raising_error_cases = [
        # wrong location label
        '',
        'a',
        '1',
        'a11',
        'bb1',
        'a9',
        'A0',
        '`3',
        'I3',
    ]

    get_vector_cases = [
        # (<src location label>,
        #  <dst location label>,
        #  <expected vector>)
        ('a1', 'a1', (0, 0)),
        ('h1', 'h1', (0, 0)),
        ('e4', 'e4', (0, 0)),
        ('a8', 'a8', (0, 0)),
        ('h8', 'h8', (0, 0)),

        ('a1', 'a2', (0, 1)),
        ('a1', 'b1', (1, 0)),
        ('a2', 'a1', (0, -1)),
        ('b1', 'a1', (-1, 0)),

        ('e4', 'e6', (0, 2)),
        ('e4', 'g4', (2, 0)),
        ('e6', 'e4', (0, -2)),
        ('g4', 'e4', (-2, 0)),
        ('e4', 'f6', (1, 2)),
        ('e4', 'g5', (2, 1)),
        ('e6', 'f4', (1, -2)),
        ('g4', 'e5', (-2, 1)),
        ('e4', 'd6', (-1, 2)),
        ('e4', 'g3', (2, -1)),
        ('e6', 'd4', (-1, -2)),
        ('g4', 'e3', (-2, -1)),
        ('e4', 'c6', (-2, 2)),
        ('e4', 'g2', (2, -2)),
        ('e6', 'c4', (-2, -2)),
        ('c4', 'e6', (2, 2)),

        ('b2', 'f2', (4, 0)),
        ('b2', 'f3', (4, 1)),
        ('b2', 'f4', (4, 2)),
        ('b2', 'f5', (4, 3)),
        ('b2', 'f6', (4, 4)),
        ('b2', 'f7', (4, 5)),

        ('f2', 'b2', (-4, 0)),
        ('f2', 'b3', (-4, 1)),
        ('f2', 'b4', (-4, 2)),
        ('f2', 'b5', (-4, 3)),
        ('f2', 'b6', (-4, 4)),
        ('f2', 'b7', (-4, 5)),

        ('a1', 'a8', (0, 7)),
        ('a1', 'h1', (7, 0)),
        ('a1', 'h8', (7, 7)),
        ('a8', 'a1', (0, -7)),
        ('h1', 'a1', (-7, 0)),
        ('h8', 'a1', (-7, -7)),
    ]

    get_path_cases = [
        # (<src location label>,
        #  <dst location label>,
        #  <labels from expected path>)
        ('a1', 'a1', []),
        ('h1', 'h1', []),
        ('e4', 'e4', []),
        ('a8', 'a8', []),
        ('h8', 'h8', []),

        ('a1', 'a2', []),
        ('a1', 'b1', []),
        ('a2', 'a1', []),
        ('b1', 'a1', []),

        ('e4', 'e6', ['e5']),
        ('e4', 'g4', ['f4']),
        ('e6', 'e4', ['e5']),
        ('g4', 'e4', ['f4']),
        ('e4', 'c6', ['d5']),
        ('e4', 'g2', ['f3']),
        ('e6', 'c4', ['d5']),
        ('c4', 'e6', ['d5']),

        ('b2', 'f2', ['c2', 'd2', 'e2']),
        ('b2', 'f6', ['c3', 'd4', 'e5']),

        ('f2', 'b2', ['e2', 'd2', 'c2']),
        ('f2', 'b6', ['e3', 'd4', 'c5']),

        ('a1', 'a8', ['a2', 'a3', 'a4', 'a5', 'a6', 'a7']),
        ('a1', 'h1', ['b1', 'c1', 'd1', 'e1', 'f1', 'g1']),
        ('a1', 'h8', ['b2', 'c3', 'd4', 'e5', 'f6', 'g7']),
        ('a8', 'a1', ['a7', 'a6', 'a5', 'a4', 'a3', 'a2']),
        ('h1', 'a1', ['g1', 'f1', 'e1', 'd1', 'c1', 'b1']),
        ('h8', 'a1', ['g7', 'f6', 'e5', 'd4', 'c3', 'b2']),
    ]

    get_path_raising_error_cases = [
        # (<src location label>, <dst location label>)
        ('e4', 'f6'),
        ('e4', 'g5'),
        ('e6', 'f4'),
        ('g4', 'e5'),
        ('e4', 'd6'),
        ('e4', 'g3'),
        ('e6', 'd4'),
        ('g4', 'e3'),

        ('b2', 'f3'),
        ('b2', 'f4'),
        ('b2', 'f5'),
        ('b2', 'f7'),

        ('f2', 'b3'),
        ('f2', 'b4'),
        ('f2', 'b5'),
        ('f2', 'b7'),
    ]

    @foreach(init_and_basics_cases)
    def test_init_and_basics(self, given_loc_label):
        loc = Location(given_loc_label)
        expected_loc_label = given_loc_label.lower()
        expected_x_label = expected_loc_label[0]
        expected_y_label = expected_loc_label[1]
        expected_repr = "Location('{}')".format(expected_loc_label)
        expected_str = expected_loc_label
        self.assertEqual(loc.loc_label, expected_loc_label)
        self.assertEqual(loc.x_label, expected_x_label)
        self.assertEqual(loc.y_label, expected_y_label)
        self.assertEqual(repr(loc), expected_repr)
        self.assertEqual(str(loc), expected_str)

    @foreach(init_raising_error_cases)
    def test_init_raising_error(self, given_loc_label):
        with self.assertRaises(InvalidLocationLabelError):
            Location(given_loc_label)

    @foreach(get_vector_cases)
    def test_get_vector(self, src_label, dst_label, expected_vector):
        src = Location(src_label)
        dst = Location(dst_label)
        actual_vector = src.get_vector(dst)
        self.assertIsInstance(actual_vector, tuple)
        self.assertEqual(actual_vector, expected_vector)

    @foreach(get_path_cases)
    def test_get_path(self, src_label, dst_label, expected_path_labels):
        src = Location(src_label)
        dst = Location(dst_label)
        actual_path = src.get_path(dst)
        actual_path_labels = [loc.loc_label for loc in actual_path]
        self.assertIsInstance(actual_path, list)
        self.assertTrue(all(isinstance(loc, Location) for loc in actual_path))
        self.assertEqual(actual_path_labels, expected_path_labels)

    @foreach(get_path_raising_error_cases)
    def test_get_path_raising_error(self, src_label, dst_label):
        src = Location(src_label)
        dst = Location(dst_label)
        with self.assertRaises(IllegalMoveError):
            src.get_path(dst)
