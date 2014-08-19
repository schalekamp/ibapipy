"""Represents a snapshot in time for an account."""


class Account:
    """Represents a snapshot in time for an account.

    Attributes not specified in the constructor:
    account_name       -- account name
    milliseconds       -- time in milliseconds since the Epoch
    net_liquidation    -- net liquidation value
    previous_equity    -- previous day's equity
    equity             -- equity with loan value
    cash               -- cash
    initial_margin     -- initial margin requirement
    maintenance_margin -- maintenance margin requirement
    available_funds    -- available funds
    excess_liquidity   -- excess liquidity
    sma                -- special memorandum account value
    buying_power       -- buying power

    """

    def __init__(self):
        """Initialize a new instance of an Account."""
        self.account_name = ''
        self.milliseconds = 0
        self.net_liquidation = 0.0
        self.previous_equity = 0.0
        self.equity = 0.0
        self.cash = 0.0
        self.initial_margin = 0.0
        self.maintenance_margin = 0.0
        self.available_funds = 0.0
        self.excess_liquidity = 0.0
        self.sma = 0.0
        self.buying_power = 0.0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Account to compare to this Account

        """
        return self.milliseconds < other.milliseconds
