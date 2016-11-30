from chess.exceptions import InvalidLocationLabelError
from chess.piece import PieceFactory


_X_LABELS = 'abcdefgh'
_Y_LABELS = '87654321'

_LABEL_TO_X = {label: x for x, label in enumerate(_X_LABELS)}
_LABEL_TO_Y = {label: y for y, label in enumerate(_Y_LABELS)}


class Board(object):

    def __init__(self):
        self._piece_factory = PieceFactory()
        self._rows_of_fields = [[None for _ in _X_LABELS]
                                for _ in xrange(_Y_LABELS)]

    def setup(self):
        self.set_row_from_symbols('8', 'rnbqkbnr')
        self.set_row_from_symbols('7', 'pppppppp')
        self.set_row_from_symbols('2', 'PPPPPPPP')
        self.set_row_from_symbols('1', 'RNBQKBNR')

    def set_row_from_symbols(self, y_label, symbols):
        if len(symbols) != len(_X_LABELS):
            raise ValueError('wrong number of symbols: {} (should be {})'.format(
                len(symbols),
                len(_X_LABELS)))
        y = _LABEL_TO_Y[y_label]
        self._rows_of_fields[y][:] = [self._piece_factory(s)
                                      for s in symbols]

    def __getitem__(self, loc):
        self._rows_of_fields[loc._y][loc._x]

    def __delitem__(self, loc):
        self._rows_of_fields[loc._y][loc._x] = None

    def __setitem__(self, loc, piece):
        self._rows_of_fields[loc._y][loc._x] = piece

    def iter_rows(self):
        return (tuple(row) for row in self._rows_of_fields)

    @staticmethod
    def iter_x_labels():
        return iter(_X_LABELS)

    @staticmethod
    def iter_y_labels():
        return iter(_Y_LABELS)


class Location(object):

    def __init__(self, loc_label):
        loc_label = loc_label.lower()
        self._x, self._y = self._parse_loc_label(loc_label)
        self.loc_label = loc_label

    def _parse_loc_label(self, loc_label):
        try:
            x_label, y_label = loc_label
            x = _LABEL_TO_X[x_label]
            y = _LABEL_TO_Y[y_label]
        except (ValueError, KeyError):
            raise InvalidLocationLabelError(
                '{!r} is not a valid location label'.format(loc_label))
        return x, y

    def get_vector(self, loc):
        return (loc._x - self._x,
                loc._y - self._y)

    def get_path(self, loc):
        TODO
