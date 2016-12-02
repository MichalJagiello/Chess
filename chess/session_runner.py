from chess.drawer import Drawer
from chess.exceptions import UserActionError
from chess.session import (
    ChessGameSession,
    QueensPuzzleSession,
)
from chess.ui import UserInput


class SessionRunner(UserInput):

    session_class = None   # must be set in subclasses

    def __init__(self):
        self.session = self.session_class()
        self.drawer = Drawer()

    def run(self):
        try:
            self.session.setup()
            self.at_start()
            self.main()
        finally:
            self.at_end()

    def main(self):
        # flag indicates weather it is a new turn and the board should
        # be displayed, or the last move was incorrect, then try again
        is_new_turn = True
        while True:
            if is_new_turn:
                self.drawer.show(self.session)
            try:
                action_arg = self.get_action_arg()
                session_finished = self.session.act(action_arg)
            except UserActionError as exc:
                is_new_turn = False
                print exc
            else:
                if session_finished:
                    break
                is_new_turn = True

    def at_start(self):
        print '\nStarting...\n'

    def get_action_arg(self):
        raise NotImplementedError

    def at_end(self):
        print '\nGood bye.\n'


class ChessGameSessionRunner(object):

    session_class = ChessGameSession

    _input_msg_pattern = '{}\'s move: (please enter something like "b4 d6" or "0-0-0"...):'

    def at_start(self):
        print '\nStarting a chess game...\n'

    def get_action_arg(self):
        input_msg = self._input_msg_pattern.format(self.session.current_player)
        user_input = self.input(input_msg)
        return map(str.strip, user_input.split())


class QueensPuzzleSessionRunner(object):

    session_class = QueensPuzzleSession

    _input_msg = 'Please, place a queen (enter something like "b4"):'

    def at_start(self):
        print '\nStarting the 8-queens puzzle...'

    def get_action_arg(self):
        return self.input(self._input_msg)