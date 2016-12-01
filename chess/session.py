from chess.board_loc import Board
from chess.move import MoveFactory
from chess.player import Player


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

    def __init__(self, *args, **kwargs):
        super(QueensPuzzleSession, self).__init__(*args, **kwargs)
        self._queen_count = 0
        #self._queen_resolver = 

    def setup(self):
        pass

    def act(self, action_spec_list):
        TODO
        # try:
        #     [loc_label] = action_spec_list
        # except (ValueError, :
        # self._set_queen(

    def _set_queen(self, dst):
        TODO
