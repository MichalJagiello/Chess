

class QueenResolver(object):

    def __init__(self):
        self._reserved_fields = []

    def is_usable_field(self, field):
        """
        Returns boolean value if field is usable to set.
        """
        pass

    def reserve_field(self, field):
        """
        Reserve given field
        """
        pass
