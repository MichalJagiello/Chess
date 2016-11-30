from chess.exceptions import IllegalMoveError


class Mover(object):

    def __init__(self):
        pass

    def do_move(self, session, move):
        field = session.board
        if field[move.src]:
            raise IllegalMoveError('Empty field {}'.format(move.src))

        field[move.dst] = field.pi
        field[move.src] = None



