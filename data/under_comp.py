"""Represents a under comp (and that is?)."""


class UnderComp:
    """Represents an ... under comp.

    Attributes not specified in the constructor:
    con_id --
    delta  --
    price  --

    """

    def __init__(self):
        """Initialize a new instance of an UnderComp."""
        self.con_id = 0
        self.delta = 0.0
        self.price = 0.0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- UnderComp to compare to this UnderComp

        """
        return self.con_id < other.con_id
