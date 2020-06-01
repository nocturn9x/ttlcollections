

class TTLItem(object):

    """An abstraction layer over a TTLed item. This class is meant
       to be used internally and should not be instantiated directly

       :param obj: The object to be wrapped
       :type obj: object
       :param date: The expiration date
       :type date: float
    """

    def __init__(self, obj: object, date: float):
        """Object constructor"""

        self.obj = obj
        self.date = date

    def __lt__(self, other):
        if isinstance(other, TTLItem):
            other = other.obj
        return self.obj.__lt__(other)

    def __eq__(self, other):
        if isinstance(other, TTLItem):
            other = other.obj
        return self.obj.__eq__(other)
