import sys

from chess.drawer import Drawer
from chess.exceptions import UserError
from chess.session import (
    ChessGameSession,
    QueensPuzzleSession,
)


class ChessMajsterGame(object):

    _action_item_separator = ' '
    _exit_game_cmd = 'exit'
    _exit_msg = 'Game has been quit by the user.'

    def __init__(self):
        self.drawer = Drawer()
        self.session = None

    def run(self):
        self.welcome()
        session_runner = self.choose_session_runner()
        session_runner()
        self.good_bye()

    def welcome(self):
        print "#############################"
        print "# Welcome to Chess Majster! #"
        print "#############################\n"
        print ("Type {0} (or Ctrl+D, or Ctrl+C) at any time "
               "to quit the game.".format(self._exit_game_cmd))

    def good_bye(self):
        print '\nGame finished. Good bye! :-)'

    def choose_session_runner(self):
        while True:
            print '\nPlease, choose the kind of session:'
            print '1) chess game'
            print '2) queens puzzle'
            print
            choice = self._input('Your choice:')
            if choice == '1':
                return self.run_chess_game
            elif choice == '2':
                return self.run_queens_puzzle
            else:
                print '1 or 2 expected...\n'

    def run_chess_game(self):
        print '\nStarting a chess game...\n'
        white_player_name = self._get_player_name('White')
        black_player_name = self._get_player_name('Black')
        self.session = ChessGameSession(white_player_name,  black_player_name)
        self.session.setup()
        self._play_turns()

    def run_queens_puzzle(self):
        print '\nStarting the 8-queens puzzle...'
        self.session = QueensPuzzleSession(player_name='Puzzle Detective')
        self.session.setup()
        self._play_turns()

    def _get_player_name(self, player_color):
        while True:
            player_name = self._input(
                'Please, enter the name for the '
                'player {0}:'.format(player_color))
            if player_name:
                return player_name
            print 'You did not enter a proper name.'

    def _play_turns(self):
        # flag indicates weather it is a new turn and the board should
        # be displayed, or the last move was incorrect, then try again
        is_new_turn = True
        while True:
            if is_new_turn:
                self.drawer.show(self.session)
            try:
                self.session.act(self._get_action_spec_list())
            except UserError as exc:
                is_new_turn = False
                print exc
            else:
                is_new_turn = True

    def _get_action_spec_list(self):
        player_name = self.session.current_player.name
        player_color = 'White' if self.session.is_white_turn else 'Black'
        while True:
            raw_action = self._input(
                '{} ({}), please enter your action:'
                .format(player_name, player_color))
            return map(str.strip, raw_action.split(self._action_item_separator))

    def _input(self, msg=None):
        if msg:
            print msg,
        try:
            user_input = raw_input().strip().lower()
            if user_input.lower() == self._exit_game_cmd:
                raise EOFError
        except (EOFError, KeyboardInterrupt):
            print '\n\n', self._exit_msg
            sys.exit()
        return user_input
