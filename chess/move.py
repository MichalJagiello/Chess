from chess.board_loc import Location
from chess.exceptions import (
    IllegalMoveError,
    InvalidLocationLabelError
)
from chess.piece import Piece


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
        self.src = Location(src_label)
        self.dst = Location(dst_label)
        self._dst_label = dst_label
        self._session = session
        # raise an exception, when any of those fields are out
        # of board's range
        self.src_loc = self._session.board[self.src]
        self.dst_loc = self._session.board[self.dst]

    def get_vector(self):
        self.src.get_vector(self._dst_label)

    def get_path(self):
        self.src.get_path(self._dst_label)

    def execute(self):
        pass
        # TODO


class LeftCastlingMove(Move):
    def execute(self):
        TODO


class RightCastlingMove(Move):
    def execute(self):
        TODO
