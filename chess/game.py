from chess.session_runner import (
    ChessGameSessionRunner,
    QueensPuzzleSessionRunner,
)


class ChessMajsterGame(UserInput):

    def run(self):
        self.welcome()
        session_runner = self.choose_session_runner()
        session_runner.run()

    def welcome(self):
        print "#############################"
        print "# Welcome to Chess Majster! #"
        print "#############################\n"
        print ("Type {0} (or Ctrl+D, or Ctrl+C) at any time "
               "to quit the game.".format(self.exit_game_cmd))

    def choose_session_runner(self):
        while True:
            print '\nPlease, choose the kind of session:'
            print '1) chess game'
            print '2) queens puzzle'
            print
            choice = self.input('Your choice:')
            if choice == '1':
                return ChessGameSessionRunner()
            elif choice == '2':
                return QueensPuzzleSessionRunner()
            else:
                print '1 or 2 expected...\n'
