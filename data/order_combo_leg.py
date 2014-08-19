"""Represents an order combination leg."""
import ibapipy.config as config


class OrderComboLeg:
    """Represents an order combination leg.

    Attributes not specified in the constructor:

    """

    def __init__(self, price=config.JAVA_DOUBLE_MAX):
        """Initialize a new instance of an OrderComboLeg.

        Keyword arguments:
        ...

        """
        self.price = price

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- ComboLeg to compare to this ComboLeg

        """
        return self.price < other.price
