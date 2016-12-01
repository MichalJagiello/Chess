class ChessError(Exception):

    default_msg = None

    def __init__(self, msg=None, *args):
        if msg is None:
            msg = self.default_msg
        super(ChessError, self).__init__(msg, *args)


class IllegalMoveError(ChessError):
    default_msg = 'The requested move is illegal.'


class InvalidLocationLabelError(ChessError):
    default_msg = 'The location label is not valid.'
