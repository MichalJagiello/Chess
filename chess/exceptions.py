class ChessError(Exception):
    """
    The base error class.
    """


class InvalidLocationLabelError(ChessError):
    """
    Raised when a location label is not valid.
    """


class InvalidPieceSymbolError(ChessError):
    """
    Raised when a piece symbol is not valid.
    """


class IllegalMoveError(ChessError):
    """
    Raised when a move requested by a player is not legal.
    """
