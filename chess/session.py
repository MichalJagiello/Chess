from chess.board_loc import Board
from chess.move import MoveFactory
from chess.player import Player


class Session(object):

    def __init__(self, white_name, black_name):
        self.last_move = None
        self.is_white_turn = True
        self.players = {
            True: Player(white_name),
            False: Player(black_name)
        }
        self.board = Board()
        self._mover_factory = MoveFactory()

    @property
    def current_player(self):
        return self.players[self.is_white_turn]

    def setup(self):
        self.board.setup()

    def do_move(self, move_label):

        move = self._mover_factory.create(self, move_label)
        move.execute()
        self.last_move = move
        self.is_white_turn = not self.is_white_turn
