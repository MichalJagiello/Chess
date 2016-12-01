from itertools import product

from chess.exceptions import IllegalMoveError, InvalidPieceSymbolError
from chess.route import Route


class PieceFactory(object):

    def __init__(self):
        self.symbols_dir = {}
        pieces = [Pawn, Knight, Bishop, Rook, Queen, King]
        for piece, is_white in product(pieces, [True, False]):
            if is_white:
                symbol = piece._raw_symbol.upper()
            else:
                symbol = piece._raw_symbol.lower()
            self.symbols_dir[symbol] = piece(is_white)

    def create(self, symbol):
        """
        Create a piece by it's symbol.

        :param symbol: Symbol of the piece
        :return: Piece
        """
        try:
            return self.symbols_dir[symbol]
        except KeyError:
            raise InvalidPieceSymbolError


class Piece(object):

    _raw_symbol = None

    def __init__(self, is_white):
        self.is_white = is_white

    def get_route(self, move):
        """
        Get piece's route for given move.

        :param move: Move
        :return: List of Locations
        """
        raise NotImplementedError()

    def get_symbol(self):
        """
        Get piece's symbol (it depends of it's color).

        :return:
        """
        if self.is_white:
            return self._raw_symbol.upper()
        return self._raw_symbol.lower()


class Pawn(Piece):

    _raw_symbol = 'P'

    def get_route(self, move):
        vector = move.src.get_vector(move.dst)
        try:
            self._check_vector_y_length(vector, self._first_move(move))
            self._check_vector_direction(vector)
        except ValueError:
            raise IllegalMoveError
        path = move.src.get_path(move.dst)
        if self._is_attack(vector):
            return Route(path, must_be_attack=True, must_not_be_attack=False)
        return Route(path, must_be_attack=False, must_not_be_attack=True)

    def _first_move(self, move):
        """
        Checks if given move is a first move
        for a pawn
        """
        if self.is_white:
            return move.src.loc_label[1] == "2"
        return move.src.loc_label[1] == "7"

    def _check_vector_y_length(self, vector, first_move):
        """
        Pawn can move only by one field if it
        is not it's first move. Otherwise
        it can move by two fields.
        """
        vector_y = abs(vector[1])
        if first_move:
            if not 0 < vector_y <= 2:
                raise ValueError
        else:
            if vector_y != 1:
                raise ValueError

    def _check_vector_direction(self, vector):
        """
        Pawn move direction depends on it's color.
        It can move up if it's white. Down otherwise
        """
        if vector[1] * (-1) ** int(self.is_white) > 0:
            raise ValueError

    def _is_attack(self, vector):
        """
        Return True if move is an attack
        """
        return all(vector)


class Knight(Piece):

    _raw_symbol = 'N'

    def get_route(self, move):
        vector = move.src.get_vector(move.dst)
        if [1, 2] != sorted(map(abs, vector)):
            raise IllegalMoveError
        return Route([])


class Bishop(Piece):

    _raw_symbol = 'B'

    def get_route(self, move):
        vector = move.src.get_vector(move.dst)
        if abs(vector[0]) != abs(vector[1]):
            raise IllegalMoveError
        return Route(move.src.get_path(move.dst))

class Rook(Piece):

    _raw_symbol = 'R'


class Queen(Piece):

    _raw_symbol = 'Q'


class King(Piece):

    _raw_symbol = 'K'
