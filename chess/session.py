from chess.board_loc import (
    Board,
    Location,
)
from chess.move import MoveFactory
from chess.piece import PieceFactory
from chess.resolver import QueenResolver


class Session(object):

    def __init__(self):
        self.board = Board()

    def setup(self):
        pass

    def act(self, action_spec_list):
        raise NotImplementedError


class ChessGameSession(Session):

    def __init__(self):
        super(ChessGameSession, self).__init__()
        self.players = {is_white: ChessGamePlayer(is_white)
                        for is_white in [True, False]}
        self.is_white_turn = True
        self.last_move = None
        self._move_factory = MoveFactory()

    @property
    def current_player(self):
        return self.players[self.is_white_turn]

    def setup(self):
        self.board.setup()

    def act(self, move_spec):
        self._do_move(move_spec)
        return self._is_game_finished()

    def _do_move(self, move_spec):
        move = self._move_factory.create(self, move_spec)
        move.execute()
        self.last_move = move
        self.is_white_turn = not self.is_white_turn

    def _is_game_finished(self):
        return False  # TODO something smarter :-)


class ChessGamePlayer(object):

    def __init__(self, is_white):
        self.player_label = 'White' if is_white else 'Black'
        self.can_queenside_castling = True
        self.can_kingside_castling = True

    def __str__(self):
        return self.player_label


class PuzzleSession(Session):

    """
    The base class for puzzle sessions.
    """


class QueensPuzzleSession(PuzzleSession):

    """
    The 8-queen puzzle session class.
    """

    max_queen_count = 8

    def __init__(self, *args, **kwargs):
        super(QueensPuzzleSession, self).__init__(*args, **kwargs)
        self._queen_count = 0
        self._queen_resolver = QueenResolver()
        self._queen = PieceFactory().create('Q')

    def act(self, action_spec_list):
        try:
            [loc_label] = action_spec_list
        except (ValueError, ):
            raise
        return self._set_queen(Location(loc_label))

    def _set_queen(self, dst):
        if self._queen_resolver.is_usable_field(dst):
            self._queen_resolver.reserve_field(dst, self._queen)
            self.board[dst] = self._queen
            self._queen_count += 1
            if self._queen_count == self.max_queen_count:
                return True
        return False
