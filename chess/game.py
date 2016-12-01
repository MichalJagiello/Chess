import sys

from chess.drawer import Drawer
from chess.exceptions import IllegalMoveError
from chess.session import Session


class ChessMajsterGame(object):

    COORD_SEPARATOR = ' '
    EXIT_GAME_CMD = 'exit'
    EXIT_STATUS = 'Game has been quit by user.'

    def __init__(self):
        self.drawer = None
        self.session = None

    def run(self):
        print "#############################"
        print "# Welcome to Chess Majster! #"
        print "#############################\n"
        print "Type {0} any time to quit game.".format(self.EXIT_GAME_CMD)
        white_player_name = self._get_player_name('White')
        black_player_name = self._get_player_name('Black')
        self.session = Session(white_player_name,  black_player_name)
        self.session.setup()
        self.drawer = Drawer()
        self.drawer.show(self.session)
        self._play_turns()

    def _get_player_name(self, player_color):
        print "Enter name for Player {0!s}:".format(str(player_color))
        while True:
            user_input = raw_input()
            if user_input.lower() == self.EXIT_GAME_CMD:
                sys.exit(self.EXIT_STATUS)
            if not user_input:
                print "You did not enter proper name."
            else:
                return user_input

    def _play_turns(self):
        # flag indicates weather it is a new turn and the board should
        # be displayed, or the last move was incorrect, then try again
        is_new_turn = True
        while True:
            if is_new_turn:
                self.drawer.show(self.session)
            if self.session.is_white_move:
                which_player = 'White'
            else:
                which_player = 'Black'
            src, dst = self._get_coords(which_player)
            try:
                self.session.do_move(src, dst)
            except IllegalMoveError as exc:
                is_new_turn = False
                print exc
            else:
                is_new_turn = True

    def _get_coords(self, which_player):
        while True:
            print "{0} player turn".format(which_player)
            print "Enter your move's coordinates separated by space:"
            user_input = raw_input()
            if not user_input:
                print "You did not enter proper coordinates."
            if user_input.lower() == self.EXIT_GAME_CMD:
                sys.exit(self.EXIT_STATUS)
            else:
                try:
                    src, dst = user_input.split(self.COORD_SEPARATOR)
                except ValueError:
                    print "You did not enter two proper coordinates."
                    continue
                return src, dst
