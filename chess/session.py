from collections import namedtuple

from chess.board_loc import (
    Board,
    Location,
)
from chess.mover import Mover
from chess.player import Player


Move = namedtuple('Move', 'src dst')


class Session(object):

    def __init__(self, white_name, black_name):
        self.last_move = None
        self.is_white_move = True
        self.white = Player(white_name)
        self.black = Player(black_name)
        self.board = Board()
        self._mover = Mover()

    def setup(self):
        self.board.setup()

    def do_move(self, src_label, dst_label):
        """

        :param player:
        :param src_label:
        :param dst_label:
        :return: None
        :raise: IllegalMoveError
        """

        move = Move(src=Location(src_label), dst=Location(dst_label))
        self._mover.do_move(self, move)
        self.last_move = move
        self.is_white_move = not self.is_white_move
