from chess.exceptions import IllegalMoveError


class MoveFactory(object):

    def create(self, session, move_spec):
        TODO


class Move(object):

    def __init__(self, session):
        self._session = session

    def execute(self):
        raise NotImplementedError


class NormalMove(Move):

    def __init__(self, session, src_label, dst_label):
        super(NormalMove, self).__init__(session)
        TODO

    def execute(self):
        TODO


class LeftCastlingMove(Move):

    def execute(self):
        TODO


class RightCastlingMove(Move):

    def execute(self):
        TODO
