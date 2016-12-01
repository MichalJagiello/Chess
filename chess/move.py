from chess.board_loc import Location
from chess.exceptions import (
    IllegalMoveError,
    InvalidLocationLabelError
)
from chess.piece import (
    King,
    Rook
)


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
        self._session = session
        # raise an exception, when any of those fields are out
        # of board's range
        self.src_piece = self._session.board[self.src]
        self.dst_piece = self._session.board[self.dst]
        self._check_src_not_empty(self.src_piece)
        self._check_if_player_owns_src_piece(self.src_piece)
        self.route = self.src_piece.get_route(self)
        self._player = self._session.current_player
        if isinstance(self.src_piece, King):
            if self._player.can_king_castling:
                self._player.can_king_castling = False
            if self._player.can_queen_castling:
                self._player.can_queen_castling = False
        if isinstance(self.src_piece, Rook):
            self._set_king_or_queen_castling(self.src, self._session.is_white_move)

    def get_vector(self):
        return self.src.get_vector(self.dst)

    def get_path(self):
        return self.src.get_path(self.dst)

    def execute(self):
        self.dst_piece, self.src_piece = self.src_piece, None

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

    def _set_king_or_queen_castling(self, src, is_white_move):
        label = src.loc_label.lower()
        if (is_white_move and label == 'a1') or (not is_white_move and label == 'a8'):
            self._player.can_king_castling = False
        elif (is_white_move and label == 'h1') or (not is_white_move and label == 'ah'):
            self._player.can_queen_castling = False


class LeftCastlingMove(Move):
    def execute(self):
        TODO


class RightCastlingMove(Move):
    def execute(self):
        TODO
