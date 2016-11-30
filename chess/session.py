from collections import namedtuple

from chess.board_loc import Board, Location
from chess.exceptions import IllegalMoveError
from chess.mover import Mover
from chess.player import Player


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
        try:
            move = namedtuple(src=Location(src_label), dst=Location(dst_label))
            self.last_move = move
        except Exception as exc:
            raise IllegalMoveError('Bad move from: {}, to: {}'.format(src_label, dst_label))

        if self.is_white_move:
            self._mover.do_move(self, move)
            self.is_white_move = False
        else:
            self._mover.do_move(self, move)
            self.is_white_move = True
