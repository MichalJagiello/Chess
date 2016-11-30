

from player import Player
from location import Location
# from mover import Mover()

class Session(object):
    is_white_move = True
    last_move = None

    def __init__(self):
        self.white = Player(name)
        self.black = Player(name='P2')
        self.board = Board()
        # self._mover = Mover()

    def do_move(self, player, src_spec, dst_spec):

        move = Move(Location(src_spec), Location(dst_spec))

        if self.is_white_move:
            self._mover.do_move(self.white, move)
            self.is_white_move = False
        else:
            self._mover.do_move(self.black, move)
            self.is_white_move = True
