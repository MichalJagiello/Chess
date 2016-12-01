from chess.session import Session


class Drawer(object):
    line_pattern = '{row_num} | {row} | {row_num}'
    field_sep = ' | '
    horizontal_line = '  ' + '-' * 33
    x_label_pattern = '  | {lables} |'

    def show(self, session):
        board = session.board
        x_label_bar = self.x_label_pattern.format(lables=self.field_sep.join(board.iter_x_labels()))
        print '\nPlayer: {}\n'.format(session.players)
        print x_label_bar
        print self.horizontal_line
        for i, row in enumerate(board.iter_rows()):
            row_repr = self._get_repr_row(row)
            print self.line_pattern.format(row_num=(7 - i + 1), row=self.field_sep.join(row_repr))
            print self.horizontal_line
        print x_label_bar

    def _get_repr_row(self, row):
        return (x.get_symbol() if x else ' ' for x in row)
