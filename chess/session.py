

from player import Player
# from mover import Mover()

class Session(object):
    is_white_move = True
    last_move = None

    def __init__(self):
        self.white = Player(name)
        self.black = Player(name='P2')
        # self._mover = Mover()

    def do_move(self, player, move):
        if self.is_white_move:
            self._mover.do_move(self.white, move)
            self.is_white_move = False
        else:
            self._mover.do_move(self.black, move)
            self.is_white_move = True
