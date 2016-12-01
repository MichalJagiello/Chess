class Player(object):

    def __init__(self, name):
        self.name = name
        self.can_queenside_castling = True
        self.can_kingside_castling = True
