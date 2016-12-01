class UserActionError(Exception):

    default_msg = 'The requested action is not valid.'

    def __init__(self, msg=None, *args):
        if msg is None:
            msg = self.default_msg
        super(UserActionError, self).__init__(msg, *args)
        self.msg = msg
