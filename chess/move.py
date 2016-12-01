from chess.exceptions import IllegalMoveError


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
        TODO

    def execute(self):
        TODO


class QueenCastlingMove(Move):

    notation = '0-0-0'

    def execute(self):
        TODO


class KingCastlingMove(Move):

    notation = '0-0'

    def execute(self):
        TODO
