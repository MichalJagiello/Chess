from itertools import product

from chess.exceptions import IllegalMoveError, InvalidPieceSymbolError
from chess.location import Location


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

    def __init__(self, is_white):
        super(Pawn, self).__init__(is_white)
        self.first_move = True

    def check_vector_length(self, vector):
        assert()

    def check_vector_direction(self, vector):
        """
        Piece move direction depends on it's color.
        It can move up if it's white. Down otherwise

        :param vector:
        :return:
        """
        pass

    def get_route(self, move):
        # TODO
        vector = move.src.get_vector(move.dst)
        # if vector[1] * -1 ** int(self.is_white) <


class Knight(Piece):

    _raw_symbol = 'N'


class Bishop(Piece):

    _raw_symbol = 'B'


class Rook(Piece):

    _raw_symbol = 'R'


class Queen(Piece):

    _raw_symbol = 'Q'


class King(Piece):

    _raw_symbol = 'K'
