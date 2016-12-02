#!/usr/bin/python
# -*- coding: utf-8 -*-


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

    def show(self, session):
        board = session.board
        x_label_bar = self.x_label_pattern.format(
            labels=self.field_sep.join(board.iter_x_labels()))
        print
        print self.horizontal_line_border
        print x_label_bar
        print self.horizontal_line_border
        for i, row in enumerate(board.iter_rows()):
            row_repr = self._get_repr_row(row)
            print self.row_repr_pattern.format(row_num=(8 - i), row=self.field_sep.join(row_repr))
            if i < 7:
                print self.horizontal_line
        print self.horizontal_line_border
        print x_label_bar
        print self.horizontal_line_border
        print

    def _get_repr_row(self, row):
        return ((self._get_unichr_piece_symbol(piece) if piece
                 else ' ')
                for piece in row)

    def _get_unichr_piece_symbol(self, piece):
        return unichr(self.piece_symbol_unichr_index[piece.get_symbol()])
