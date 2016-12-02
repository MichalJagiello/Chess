from chess.board_loc import Board
from chess.move import MoveFactory
from chess.player import Player
from resolver import QueenResolver
from board_loc import Location
from piece import PieceFactory


class Session(object):

    def __init__(self, player_name):
        self.board = Board()
        self.players = {
            True: Player(player_name),
        }
        self.is_white_turn = True

    @property
    def current_player(self):
        return self.players[self.is_white_turn]

    def setup(self):
        raise NotImplementedError

    def act(self, action_spec_list):
        raise NotImplementedError


class ChessGameSession(Session):

    def __init__(self, white_player_name, black_player_name):
        super(ChessGameSession, self).__init__(white_player_name)
        self.players[False] = Player(black_player_name)
        self.last_move = None
        self._move_factory = MoveFactory()

    def setup(self):
        self.board.setup()

    def act(self, action_spec_list):
        self._do_move(move_spec=action_spec_list)

    def _do_move(self, move_spec):
        move = self._move_factory.create(self, move_spec)
        move.execute()
        self.last_move = move
        self.is_white_turn = not self.is_white_turn


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

    def setup(self):
        pass

    def act(self, action_spec_list):
        try:
            [loc_label] = action_spec_list
        except (ValueError, ):
            raise

        return self._set_queen(Location(loc_label))

    def _set_queen(self, dst):

        if self._queen_resolver.is_usable_field(dst):
            self._queen_resolver.reserve_field(dst, self._queen)
            self._queen_count += 1
            if self._queen_count == self.max_queen_count:
                return True
        return False
