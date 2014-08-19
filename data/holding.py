"""Represents a single portfolio holding."""


class Holding:
    """Represents a single portfolio holding.

    Attributes not specified in the constructor:
    milliseconds -- time in milliseconds since the Epoch
    quantity     -- quantity in units
    market_price -- current market price
    market_value -- current market value
    average_cost -- average entry cost
    unrealized   -- unrealized profit or loss
    realized     -- realized profit or loss

    """

    def __init__(self, account='', local_symbol=''):
        """Initialize a new instance of a Holding.

        Keyword arguments:
        account      -- account number (default: '')
        local_symbol -- ticker symbol (default: '')

        """
        self.account = account
        self.local_symbol = local_symbol
        self.milliseconds = 0
        self.quantity = 0
        self.market_price = 0.0
        self.market_value = 0.0
        self.average_cost = 0.0
        self.unrealized = 0.0
        self.realized = 0.0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Holding to compare to this Holding

        """
        return self.milliseconds < other.milliseconds
