from chess.board_loc import Location
from chess.exceptions import IllegalMoveError
from chess.util import critical_part


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


class CastlingMove(Move):

    _is_white_to_y_label = {
        True: '2',
        False: '7',
    }

    move_error_msg = None    # must be overridden

    rook_src_x_label = None  # must be overridden
    rook_dst_x_label = None  # must be overridden

    king_src_x_label = 'e'
    king_dst_x_label = None  # must be overridden

    def execute(self):
        try:
            if not self.can_be_done():
                raise IllegalMoveError
            self._move_the_rook()
        except IllegalMoveError:
            raise IllegalMoveError(self.move_error_msg)
        with critical_part():
            # *no* exception should occur here because
            # self._move_the_rook() mutated the session
            self._move_the_king()
        self._mark_as_done()

    def can_be_done(self):
        raise NotImplementedError

    def _mark_as_done(self):
        player = self._session.current_player
        player.can_queenside_castling = False
        player.can_kingside_castling = False

    def _move_the_rook(self):
        rook_move = self._get_rook_move()
        rook_move.execute()

    def _get_rook_move(self):
        return NormalMove(
            self._session,
            self._get_rook_src_label(),
            self._get_rook_dst_label())

    def _get_rook_src_label(self):
        return Location.make_loc_label(
            self.rook_src_x_label,
            self._get_y_label())

    def _get_rook_dst_label(self):
        return Location.make_loc_label(
            self.rook_dst_x_label,
            self._get_y_label())

    def _move_the_king(self):
        board = self._session.board
        king_src = self._get_king_src()
        king_dst = self._get_king_dst()
        king = board.pop(king_src)
        board[king_dst] = king

    def _get_king_src(self):
        loc_label = Location.make_loc_label(
            self.king_src_x_label,
            self._get_y_label())
        return Location(loc_label)

    def _get_king_dst(self):
        loc_label = Location.make_loc_label(
            self.king_dst_x_label,
            self._get_y_label())
        return Location(loc_label)

    def _get_y_label(self):
        return self._is_white_to_y_label[self._session.is_white_move]


class QueensideCastlingMove(Move):

    move_error_msg = 'Queenside castling is not possible.'

    rook_src_x_label = 'a'
    rook_dst_x_label = 'd'

    king_dst_x_label = 'c'

    def can_be_done(self):
        return self._session.current_player.can_queenside_castling


class KingsideCastlingMove(Move):

    move_error_msg = 'Kingside castling is not possible.'

    rook_src_x_label = 'h'
    rook_dst_x_label = 'f'

    king_dst_x_label = 'g'

    def can_be_done(self):
        return self._session.current_player.can_kingside_castling
