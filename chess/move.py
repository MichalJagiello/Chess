from chess.board_loc import Location
from chess.exceptions import UserActionError
from chess.piece import (
    King,
    Pawn,
    Rook,
)
from chess.util import critical_part


class MoveFactory(object):

    _queenside_castling_label = '0-0-0'
    _kingside_castling_label = '0-0'

    def create(self, session, move_spec):
        from chess.session import ChessGameSession
        assert isinstance(session, ChessGameSession)
        assert isinstance(move_spec, list)
        assert all(isinstance(item, str) for item in move_spec)
        if len(move_spec) == 2:
            move = NormalMove(session, *move_spec)
        elif len(move_spec) == 1:
            if move_spec[0] == self._queenside_castling_label:
                move = QueensideCastlingMove(session)
            elif move_spec[0] == self._kingside_castling_label:
                move = KingsideCastlingMove(session)
            else:
                raise UserActionError
        else:
            raise UserActionError
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
        self.piece = session.board[self.src]
        self._session = session
        self._en_passant_attack_dst = None

    def get_vector(self):
        return self.src.get_vector(self.dst)

    def get_path(self):
        return self.src.get_path(self.dst)

    def execute(self):
        self._validate_and_prepare()
        with critical_part():
            self._mutate_board()
            self._maintain_future_castlings()

    # non-public helpers:

    def _validate_and_prepare(self):
        self._check_src_not_empty()
        self._check_if_player_owns_src_piece()
        self._check_src_dst_are_distinct()
        route = self.piece.get_route(self)
        self._check_path(route)
        self._check_dst_field(route)

    def _mutate_board(self):
        moved_piece = self._session.board.pop_piece(self.src)
        assert moved_piece is self.piece
        self._session.board[self.dst] = moved_piece
        if self._en_passant_attack_dst:
            del self._session.board[self._en_passant_attack_dst]

    def _maintain_future_castlings(self):
        player = self._session.current_player
        if self._should_disable_queenside_castlings():
            player.queenside_castling_enabled = False
        if self._should_disable_kingside_castlings():
            player.kingside_castling_enabled = False

    def _check_src_not_empty(self):
        if self.piece is None:
            raise UserActionError('Source location does not contain any figure.')

    def _check_if_player_owns_src_piece(self):
        if self.piece.is_white != self._session.is_white_turn:
            raise UserActionError('You tried to move not your piece.')

    def _check_src_dst_are_distinct(self):
        if self.get_vector() == (0, 0):
            raise UserActionError('You tried to move to the same location.')

    def _check_path(self, route):
        for loc in route.path:
            if self._session.board[loc] is not None:
                raise UserActionError('Other piece on move path.')

    def _check_dst_field(self, route):
        dst_piece = self._session.board[self.dst]
        if route.attack_required:
            if not dst_piece:
                self._check_en_passant()
            elif self.piece.is_white == dst_piece.is_white:
                raise UserActionError('This move has to be an attack.')
        if route.attack_forbidden:
            if dst_piece:
                raise UserActionError('This move can\'t be an attack.')
        if dst_piece and self.piece.is_white == dst_piece.is_white:
            raise UserActionError('You tried to attack your\'s piece.')

    def _check_en_passant(self):
        if not self._session.last_move:
            raise UserActionError('Invalid en passant attack.')
        last_move = self._session.last_move
        if not isinstance(self.piece, Pawn) or not isinstance(last_move.piece, Pawn):
            raise UserActionError('Invalid en passant attack.')
        if not self._between(
                self.dst.y_label,
                last_move.src.y_label,
                last_move.dst.y_label):
            raise UserActionError('Invalid en passant attack.')
        self._en_passant_attack_dst = last_move.dst

    def _between(self, value, first, second):
        if first < second:
            return first < value < second
        return second < value < first

    def _should_disable_queenside_castlings(self):
        is_white_turn = self._session.is_white_turn
        return isinstance(self.piece, King) or (
            isinstance(self.piece, Rook) and (
                (self.src.loc_label == 'a1' and is_white_turn) or
                (self.src.loc_label == 'a8' and not is_white_turn)))

    def _should_disable_kingside_castlings(self):
        is_white_turn = self._session.is_white_turn
        return isinstance(self.piece, King) or (
            isinstance(self.piece, Rook) and (
                (self.src.loc_label == 'h1' and is_white_turn) or
                (self.src.loc_label == 'h8' and not is_white_turn)))


class CastlingMove(Move):

    _is_white_to_y_label = {
        True: '1',
        False: '8',
    }

    move_error_msg = None    # must be overridden

    rook_src_x_label = None  # must be overridden
    rook_dst_x_label = None  # must be overridden

    king_src_x_label = 'e'
    king_dst_x_label = None  # must be overridden

    def execute(self):
        try:
            if not self.can_be_done():
                raise UserActionError
            self._move_the_rook()
        except UserActionError:
            raise UserActionError(self.move_error_msg)
        with critical_part():
            # *no* exception should occur here because
            # self._move_the_rook() mutated the session
            self._move_the_king()
            self._disable_future_castlings()

    def can_be_done(self):
        raise NotImplementedError

    def _disable_future_castlings(self):
        player = self._session.current_player
        player.queenside_castling_enabled = False
        player.kingside_castling_enabled = False

    # non-public helpers:

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
        king = board.pop_piece(king_src)
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
        return self._is_white_to_y_label[self._session.is_white_turn]


class QueensideCastlingMove(CastlingMove):

    move_error_msg = 'Queenside castling is not possible.'

    rook_src_x_label = 'a'
    rook_dst_x_label = 'd'

    king_dst_x_label = 'c'

    def can_be_done(self):
        return self._session.current_player.queenside_castling_enabled


class KingsideCastlingMove(CastlingMove):

    move_error_msg = 'Kingside castling is not possible.'

    rook_src_x_label = 'h'
    rook_dst_x_label = 'f'

    king_dst_x_label = 'g'

    def can_be_done(self):
        return self._session.current_player.kingside_castling_enabled
