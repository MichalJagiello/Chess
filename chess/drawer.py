from chess.session import Session


class Drawer(object):

    def show(self, session):
        field_sep = ' | '
        print '\nPlayer: {}\n'.format(session.white.name)
        line_symbol = '  ' + '-' * 33
        board = session.board
        x_labels = session.board.iter_x_labels()
        x_label_bar = '{x}|{lables}'.format(x='    ', lables=field_sep.join(x_labels))
        print x_label_bar
        print line_symbol
        for i, row in enumerate(board.iter_rows()):
            row_repr = self.get_repr_row(row)
            line = '{row_num} | {row} | {row_num}'
            print line.format(row_num=(7 - i + 1), row=field_sep.join(row_repr))
            print line_symbol

        print x_label_bar
    def get_repr_row(self, row):

        return (x.get_symbol() if x else 'NN' for x in row)

    def get_field_symbol(self, field):

        return field
if __name__ == '__main__':
    session = Session('White', 'Black')
    session.board.setup()
    drawer = Drawer()
    drawer.show(session)