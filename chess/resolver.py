

class QueenResolver(object):

    def __init__(self):
        self._reserved_fields = set()

    def is_usable_field(self, loc):
        """
        Returns boolean value if field is usable to set.

        :param field:
        :return: bool
        """
        return loc in self._reserved_fields

    def reserve_field(self, loc):
        """
        Reserve given field

        :param loc:
        :return:
        """
        self._reserved_fields.update(loc)
