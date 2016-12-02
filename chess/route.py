class Route(object):

    def __init__(self, path, attack_required=False, attack_forbidden=False):
        self.path = path
        self.attack_required = attack_required
        self.attack_forbidden = attack_forbidden
