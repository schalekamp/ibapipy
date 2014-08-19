"""Represents a single trade execution."""


class Execution:
    """Represents a single trade execution.

    Attributes not specified in the constructor:
    order_id    --
    client_id   --
    exec_id     --
    time        --
    acct_number --
    exchange    --
    side        --
    shares      --
    price       --
    perm_id     --
    liquidation --
    cum_qty     --
    avg_price   --
    order_ref   --

    """

    def __init__(self):
        """Initialize a new instance of an Execution."""
        self.order_id = 0
        self.client_id = 0
        self.exec_id = ''
        self.time = ''
        self.milliseconds = 0
        self.acct_number = ''
        self.exchange = ''
        self.side = ''
        self.shares = 0
        self.price = 0.0
        self.perm_id = 0
        self.liquidation = 0
        self.cum_qty = 0
        self.avg_price = 0.0
        self.order_ref = ''

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Execution to compare to this Execution

        """
        return self.milliseconds < other.milliseconds
