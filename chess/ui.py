import sys


class UserInputMixin(object):

    exit_game_cmd = 'exit'
    exit_msg = 'Quit by the user.'

    def input(self, msg=None):
        if msg:
            print msg,
        try:
            user_input = raw_input().strip().lower()
            if user_input.lower() == self.exit_game_cmd:
                raise EOFError
        except (EOFError, KeyboardInterrupt):
            print '\n\n', self.exit_msg
            sys.exit()
        return user_input


class Drawer(object):

    row_repr_pattern = u'{row_num} | {row} | {row_num}'
    field_sep = u' | '
    horizontal_line = u'  ' + u'-' * 33
    horizontal_line_border = u'  ' + u'=' * 33

    x_label_pattern = u'  | {labels} |'
    piece_symbol_unichr_index = {
        'k': 9812,
        'q': 9813,
        'r': 9814,
        'b': 9815,
        'n': 9816,
        'p': 9817,
        'K': 9818,
        'Q': 9819,
        'R': 9820,
        'B': 9821,
        'N': 9822,
        'P': 9823,
    }

    def __init__(self, session_runner):
        self._board = session_runner.session.board
        self._x_label_bar = self.x_label_pattern.format(
            labels=self.field_sep.join(self._board.iter_x_labels()))

    def show(self):
        self._show_top()
        for i, row in enumerate(self._board.iter_rows()):
            self._show_row(i, row)
        self._show_bottom()

    def _show_row(self, i, row):
        row_repr = self._get_repr_row(row)
        print self.row_repr_pattern.format(
            row_num=(8 - i),
            row=self.field_sep.join(row_repr))
        if i < 7:
            print self.horizontal_line

    def _show_top(self):
        print
        self._show_bar()

    def _show_bottom(self):
        self._show_bar()
        print

    def _show_bar(self):
        print self.horizontal_line_border
        print self._x_label_bar
        print self.horizontal_line_border

    def _get_repr_row(self, row):
        return ((self._get_unichr_piece_symbol(piece) if piece
                 else ' ')
                for piece in row)

    def _get_unichr_piece_symbol(self, piece):
        return unichr(self.piece_symbol_unichr_index[piece.get_symbol()])
