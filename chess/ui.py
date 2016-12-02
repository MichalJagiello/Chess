import sys


class UserInput(object):

    exit_game_cmd = 'exit'

    _exit_msg = 'Quit by the user.'

    def input(self, msg=None):
        if msg:
            print msg,
        try:
            user_input = raw_input().strip().lower()
            if user_input.lower() == self.exit_game_cmd:
                raise EOFError
        except (EOFError, KeyboardInterrupt):
            print '\n\n', self._exit_msg
            sys.exit()
        return user_input
