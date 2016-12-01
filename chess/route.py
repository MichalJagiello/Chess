from chess.board_loc import Location


class Route(object):

    def __init__(self, path, must_be_attack=False, must_not_be_attack=False):
        assert all(isinstance(loc, Location) for loc in path)
        self.path = path
        self.must_be_attack = must_be_attack
        self.must_not_be_attack = must_not_be_attack