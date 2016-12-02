from itertools import product

from chess.board_loc import Board, Location
from chess.exceptions import UserActionError
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
        return self.symbols_dir[symbol]


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

    def get_attacked_locations(self, location):
        """
        Get the iterator with locations which can
        be attacked by piece for given location.
        """
        raise NotImplementedError()

    @staticmethod
    def _get_left_diagonal_negative_attack_locations(location):

        x_symbol = location.x_label
        y_symbol = location.y_label
        while x_symbol != 'a' and y_symbol != '1':
            x_symbol = chr(ord(x_symbol) - 1)
            y_symbol = chr(ord(y_symbol) - 1)
            yield Location("{}{}".format(x_symbol, y_symbol))

    @staticmethod
    def _get_left_diagonal_positive_attack_locations(location):

        x_symbol = location.x_label
        y_symbol = location.y_label
        while x_symbol != 'a' and y_symbol != '8':
            x_symbol = chr(ord(x_symbol) - 1)
            y_symbol = chr(ord(y_symbol) + 1)
            yield Location("{}{}".format(x_symbol, y_symbol))

    @staticmethod
    def _get_right_diagonal_negative_attack_locations(location):

        x_symbol = location.x_label
        y_symbol = location.y_label
        while x_symbol != 'h' and y_symbol != '1':
            x_symbol = chr(ord(x_symbol) + 1)
            y_symbol = chr(ord(y_symbol) - 1)
            yield Location("{}{}".format(x_symbol, y_symbol))

    @staticmethod
    def _get_right_diagonal_positive_attack_locations(location):

        x_symbol = location.x_label
        y_symbol = location.y_label
        while x_symbol != 'h' and y_symbol != '8':
            x_symbol = chr(ord(x_symbol) + 1)
            y_symbol = chr(ord(y_symbol) + 1)
            yield Location("{}{}".format(x_symbol, y_symbol))

    @classmethod
    def _get_diagonal_attack_locations(cls, location):

        left_diagonal_negative_locations = {location for location in
                                            cls._get_left_diagonal_negative_attack_locations(location)}
        left_diagonal_positive_locations = {location for location in
                                            cls._get_left_diagonal_positive_attack_locations(location)}
        right_diagonal_negative_locations = {location for location in
                                             cls._get_right_diagonal_negative_attack_locations(location)}
        right_diagonal_positive_locations = {location for location in
                                             cls._get_right_diagonal_positive_attack_locations(location)}
        return list(left_diagonal_negative_locations ^ left_diagonal_positive_locations ^
                    right_diagonal_negative_locations ^ right_diagonal_positive_locations)

    @classmethod
    def _get_straight_line_attack_locations(cls, location):

        x_line_locs_set = {Location("{}{}".format(*loc_label))
                           for loc_label in product(location.x_label, Board.iter_y_labels())}
        y_line_locs_set = {Location("{}{}".format(*loc_label))
                           for loc_label in product(Board.iter_x_labels(), location.y_label)}

        return list(x_line_locs_set ^ y_line_locs_set)


class Pawn(Piece):

    _raw_symbol = 'P'

    def get_route(self, move):
        vector = move.get_vector()
        try:
            self._check_vector_y_length(vector, self._first_move(move))
            self._check_vector_direction(vector)
        except ValueError:
            raise UserActionError
        path = move.get_path()
        if self._is_attack(vector):
            return Route(path, attack_required=True, attack_forbidden=False)
        return Route(path, attack_required=False, attack_forbidden=True)

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
        if all(vector):
            if abs(vector[0]) != 1 and abs(vector[1]) != 1:
                raise UserActionError
            return True
        return False


class Knight(Piece):

    _raw_symbol = 'N'

    def get_route(self, move):
        vector = move.get_vector()
        if [1, 2] != sorted(map(abs, vector)):
            raise UserActionError
        return Route([])


class Bishop(Piece):

    _raw_symbol = 'B'

    def get_route(self, move):
        vector = move.get_vector()
        if abs(vector[0]) != abs(vector[1]):
            raise UserActionError
        return Route(move.get_path())

    def get_attacked_locations(self, location):
        return self._get_diagonal_attack_locations(location)


class Rook(Piece):

    _raw_symbol = 'R'

    def get_route(self, move):
        vector = move.get_vector()
        if 0 in vector:
            return Route(move.get_path())
        raise UserActionError

    def get_attacked_locations(self, location):
        return self._get_straight_line_attack_locations(location)


class Queen(Piece):

    _raw_symbol = 'Q'

    def get_route(self, move):
        vector = move.get_vector()

        if all(vector):
            if abs(vector[0]) != abs(vector[1]):
                raise UserActionError

        return Route(move.get_path())

    def get_attacked_locations(self, location):
        _straight_line_attack_locations = self._get_straight_line_attack_locations(location)
        _diagonal_attack_locations = self._get_diagonal_attack_locations(location)

        return list(set(_straight_line_attack_locations) ^ set(_diagonal_attack_locations))


class King(Piece):

    _raw_symbol = 'K'

    def get_route(self, move):
        vector = move.get_vector()
        if any(i > 1 for i in map(abs, vector)):
            raise UserActionError
        return Route(move.get_path())
