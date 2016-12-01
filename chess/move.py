from chess.board_loc import Location
from chess.exceptions import IllegalMoveError
from chess.piece import (
    King,
    Rook
)
from chess.util import critical_part


class MoveFactory(object):

    _queenside_castling_label = '0-0-0'
    _kingside_castling_label = '0-0'

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
            if move_spec[0] == self._queenside_castling_label:
                move = QueensideCastlingMove(session)
            elif move_spec[0] == self._kingside_castling_label:
                move = KingsideCastlingMove(session)
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
        self._session = session
        # raise an exception, when any of those fields are out
        # of board's range
        self.src_piece = self._session.board[self.src]
        self.dst_piece = self._session.board[self.dst]

    def get_vector(self):
        return self.src.get_vector(self.dst)

    def get_path(self):
        return self.src.get_path(self.dst)

    def execute(self):
        self._check_src_not_empty(self.src_piece)
        self._check_if_player_owns_src_piece(self.src_piece)
        self.route = self.src_piece.get_route(self)
        self._check_dst_field()
        self._player = self._session.current_player
        self._session.board[self.dst] = self._session.board.pop(self.src)
        if isinstance(self.dst_piece, King):
            if self._player.can_kingside_castling:
                self._player.can_kingside_castling = False
            if self._player.can_queenside_castling:
                self._player.can_queenside_castling = False
        if isinstance(self.src_piece, Rook):
            self._set_king_or_queenside_castling(self.src, self._session.is_white_move)

    @staticmethod
    def _check_src_not_empty(piece):
        if piece is None:
            raise IllegalMoveError('Source location does not contain any figure.')

    def _check_if_player_owns_src_piece(self, piece):
        if piece.is_white != self._session.is_white_move:
            raise IllegalMoveError('You tried to move not your piece.')

    def _check_src_dst_are_different(self):
        if not any(self.get_vector()):
            raise IllegalMoveError('You tried to move on the same location.')

    def _check_path(self):
        for field in self.route:
            if self._session.board[field] is not None:
                raise IllegalMoveError('Other piece on move path')

    def _set_king_or_queenside_castling(self, src, is_white_move):
        label = src.loc_label.lower()
        if (is_white_move and label == 'a1') or (not is_white_move and label == 'a8'):
            self._player.can_queenside_castling = False
        elif (is_white_move and label == 'h1') or (not is_white_move and label == 'ah'):
            self._player.can_kingside_castling = False

    def _check_dst_field(self):
        if self.route.must_be_attack:
            if not self.dst_piece or self.src_piece.is_white == self.dst_piece.is_white:
                raise IllegalMoveError('This move has to be an attack')
        if self.route.must_not_be_attack:
            if self.dst_piece:
                raise IllegalMoveError('This move can\'t be an attack')
        if self.dst_piece and self.src_piece.is_white == self.dst_piece.is_white:
            raise IllegalMoveError('You tried to attack your\'s piece')


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
