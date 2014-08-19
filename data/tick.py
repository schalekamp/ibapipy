"""Represents a tick (bid/ask) of pricing data."""


class Tick:
    """Represents a tick (bid/ask) of pricing data.

    Attributes not specified in the constructor:
    bid      -- bid price
    ask      -- ask price
    bid_size -- size of the bid
    ask_size -- size of the ask
    volume   -- shares or units traded

    """

    def __init__(self, local_symbol='', milliseconds=0):
        """Initialize a new instance of a Tick.

        Keyword arguments:
        local_symbol -- ticker symbol
        milliseconds -- time in milliseconds since the Epoch

        """
        self.local_symbol = local_symbol
        self.milliseconds = milliseconds
        self.bid = 0.0
        self.ask = 0.0
        self.bid_size = 0
        self.ask_size = 0
        self.volume = 0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Tick to compare to this Tick

        """
        return self.milliseconds < other.milliseconds

    def midpoint(self):
        """Return the midpoint between the bid and ask prices."""
        return (self.ask + self.bid) * 0.5

    def spread(self):
        """Return the difference between the bid and ask prices."""
        return self.ask - self.bid
