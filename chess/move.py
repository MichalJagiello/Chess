from chess.board_loc import Location
from chess.exceptions import (
    IllegalMoveError,
    InvalidLocationLabelError
)
from chess.piece import Piece


class MoveFactory(object):

    def create(self, session, move_spec):
        """

        :param session:
        :param move_spec:
        :return: move
        :raise: IllegalMoveError
        """

        assert isinstance(move_spec, list)

        if len(move_spec) == 2:
            move = NormalMove(session, move_spec[0],  move_spec[1])
        elif len(move_spec) == 1:
            if move_spec[0] == QueenCastlingMove.notation:
                move = QueenCastlingMove(session)
            elif move_spec[0] == KingCastlingMove.notation:
                move = KingCastlingMove(session)
            else:
                # not implemented notation
                raise IllegalMoveError
        else:
            # not implemented notation
            raise IllegalMoveError

        return move


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
        return self.src.get_vector(self._dst_label)

    def get_path(self):
        return self.src.get_path(self._dst_label)

    def execute(self):
        pass
        # TODO

    def _check_src_dst_are_different(self):
        if not any(self.get_vector()):
            raise IllegalMoveError('You tried to move on the same location.')


class QueenCastlingMove(Move):

    notation = '0-0-0'


class KingCastlingMove(Move):

    notation = '0-0'

