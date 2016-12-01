from collections import namedtuple

from chess.exceptions import IllegalMoveError
from chess.piece import (
    Piece,
    PieceFactory,
)


_X_LABELS = 'abcdefgh'
_Y_LABELS = '87654321'

_LABEL_TO_X = {label: x for x, label in enumerate(_X_LABELS)}
_LABEL_TO_Y = {label: y for y, label in enumerate(_Y_LABELS)}


Move = namedtuple('Move', ['src', 'dst'])


class Board(object):

    def __init__(self):
        self._piece_factory = PieceFactory()
        self._rows_of_fields = [[None for _ in _X_LABELS]
                                for _ in _Y_LABELS]

    def setup(self):
        self._set_row_from_symbols('8', 'rnbqkbnr')
        self._set_row_from_symbols('7', 'pppppppp')
        self._set_row_from_symbols('2', 'PPPPPPPP')
        self._set_row_from_symbols('1', 'RNBQKBNR')

    def __getitem__(self, loc):
        assert isinstance(loc, Location)
        return self._rows_of_fields[loc._y][loc._x]

    def __setitem__(self, loc, piece):
        assert isinstance(loc, Location)
        assert isinstance(piece, Piece)
        self._rows_of_fields[loc._y][loc._x] = piece

    def __delitem__(self, loc):
        assert isinstance(loc, Location)
        self._rows_of_fields[loc._y][loc._x] = None

    def pop_piece(self, loc):
        f = self[loc]
        del self[loc]
        return f

    def iter_rows(self):
        return (tuple(row) for row in self._rows_of_fields)

    @staticmethod
    def iter_x_labels():
        return iter(_X_LABELS)

    @staticmethod
    def iter_y_labels():
        return iter(_Y_LABELS)

    # non-public helpers:

    def _set_row_from_symbols(self, y_label, symbols):
        assert len(symbols) == len(_X_LABELS), (
            'wrong number of symbols: {} -- '
            'should be {} ({!r} vs. {!r})'.format(
                len(symbols),
                len(_X_LABELS),
                symbols,
                _X_LABELS))
        y = Location._parse_y_label(y_label)
        self._rows_of_fields[y][:] = [
            (None if s == ' ' else self._piece_factory.create(s))
            for s in symbols]


class Location(object):

    def __init__(self, loc_label):
        assert isinstance(loc_label, str)
        self.loc_label = loc_label.lower()
        (self.x_label,
         self.y_label,
         self._x,
         self._y) = self._parse_loc_label(self.loc_label)

    def __repr__(self):
        return '{0.__class__.__name__}({0.loc_label!r})'.format(self)

    def __str__(self):
        return self.loc_label

    def __eq__(self, other):
        return self.loc_label == other.loc_label

    def __ne__(self, other):
        return self.loc_label != other.loc_label

    def __hash__(self):
        return hash(self.loc_label)

    def get_vector(self, dst):
        assert isinstance(dst, Location)
        return (dst._x - self._x,
                self._y - dst._y)  # inversion: white low, black high

    def get_path(self, dst):
        assert isinstance(dst, Location)
        return list(self._iter_intermediate_locations(dst))

    @staticmethod
    def make_loc_label(x_label, y_label):
        return '{}{}'.format(x_label, y_label)

    # non-public helpers:

    def _parse_loc_label(self, loc_label):
        try:
            x_label, y_label = loc_label
            x = self._parse_x_label(x_label)
            y = self._parse_y_label(y_label)
        except (ValueError, KeyError):
            raise IllegalMoveError(
                '{!r} is not a valid location label.'.format(loc_label))
        return x_label, y_label, x, y

    @staticmethod
    def _parse_x_label(x_label):
        return _LABEL_TO_X[x_label]

    @staticmethod
    def _parse_y_label(y_label):
        return _LABEL_TO_Y[y_label]

    def _iter_intermediate_locations(self, dst):
        x = self._x
        y = self._y
        x_delta = dst._x - x
        y_delta = dst._y - y
        if not self._in_straight_line(x_delta, y_delta):
            raise IllegalMoveError
        x_step = self._delta_to_step(x_delta)
        y_step = self._delta_to_step(y_delta)
        while True:
            x += x_step
            y += y_step
            assert (0 <= x <= len(_X_LABELS) and
                    0 <= y <= len(_Y_LABELS))
            if (x, y) == (dst._x, dst._y):
                break
            yield self._new_from_x_y(x, y)

    def _in_straight_line(self, x_delta, y_delta):
        return (x_delta == 0 or
                y_delta == 0 or
                abs(x_delta) == abs(y_delta))

    def _delta_to_step(self, delta):
        step = min(1, max(-1, delta))
        assert -1 <= step <= 1
        return step

    @classmethod
    def _new_from_x_y(cls, x, y):
        loc_label = cls.make_loc_label(_X_LABELS[x], _Y_LABELS[y])
        return cls(loc_label)
