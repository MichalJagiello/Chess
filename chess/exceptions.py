class UserError(Exception):

    default_msg = None

    def __init__(self, msg=None, *args):
        if msg is None:
            msg = self.default_msg or 'No, try again...'
        super(UserError, self).__init__(msg, *args)


class IllegalMoveError(UserError):
    default_msg = 'The requested move is illegal.'
