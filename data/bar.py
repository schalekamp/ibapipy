"""Represents pricing data for a given block of time."""


class Bar:
    """Represents pricing data for a given block of time.

    Attributes not specified in the constructor:
    open   -- opening price for the time period
    high   -- closing price
    low    -- low price
    close  -- close price
    volume -- volume
    count  -- number of trades

    """

    def __init__(self, local_symbol, milliseconds):
        """Initialize a new instance of a Bar.

        Keyword arguments:
        local_symbol -- ticker symbol
        milliseconds -- time in milliseconds since the Epoch

        """
        self.local_symbol = local_symbol
        self.milliseconds = milliseconds
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.volume = 0
        self.count = 0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Bar to compare to this Bar

        """
        return self.milliseconds < other.milliseconds
