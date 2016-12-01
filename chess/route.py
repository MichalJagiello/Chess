class Route(object):

    def __init__(self, path, must_be_attack=False, must_not_be_attack=False):
        self.path = path
        self.must_be_attack = must_be_attack
        self.must_not_be_attack = must_not_be_attack