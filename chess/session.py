
from collections import namedtuple

from player import Player
from location import Location
from board import Board
# from mover import Mover()


class Session(object):
    is_white_move = True
    last_move = None

    def __init__(self, white_name, black_name):
        self.white = Player(white_name)
        self.black = Player(black_name)
        self.board = Board()
        # self._mover = Mover()

    def do_move(self, player, src_spec, dst_spec):
        move = namedtuple(**{'src': Location(src_spec), 'dst': Location(dst_spec)})

        if self.is_white_move:
            self._mover.do_move(self.white, move)
            self.is_white_move = False
        else:
            self._mover.do_move(self.black, move)
            self.is_white_move = True
