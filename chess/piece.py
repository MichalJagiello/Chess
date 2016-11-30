
class Piece(object):

    def __init__(self, is_white):
        self.is_white = is_white

    def get_route(self, move):
        """
        Get piece's route for given move.

        :param move: Move
        :return: List of Locations
        """
        raise NotImplementedError()


class Pawn(Piece):

    symbol = 'P'


class Knight(Piece):

    symbol = 'N'


class Bishop(Piece):

    symbol = 'B'


class Rook(Piece):

    symbol = 'R'


class Queen(Piece):

    symbol = 'Q'


class King(Piece):

    symbol = 'K'
