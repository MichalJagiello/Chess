

class IllegalMoveError(Exception):
    """
    Raised when invalid move was requested by a player
    """


class InvalidPieceSymbolError(Exception):
    """
    Raised when invalid piece symbol
    was given to piece factory.
    """