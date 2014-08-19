"""Represents an execution filter."""


class ExecutionFilter:
    """Represents an execution filter.

    Attributes not specified in the constructor:
    client_id --
    acct_code --
    time      --
    symbol    --
    sec_type  --
    exchange  --
    side      --

    """

    def __init__(self):
        """Initialize a new instance of an ExecutionFilter."""
        self.client_id = 0
        self.acct_code = ''
        self.time = ''
        self.symbol = ''
        self.sec_type = ''
        self.exchange = ''
        self.side = ''
