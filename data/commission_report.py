"""Represents a commission report."""


class CommissionReport:
    """Represents a commission reoprt.

    Attributes not specified in the constructor:
    exec_id               --
    commission            --
    currency              --
    realized_pnl          --
    yield_value           --
    yield_redemption_date --

    """

    def __init__(self):
        """Initialize a new instance of a CommissionReport.

        Keyword arguments:
        ...

        """
        self.exec_id = ''
        self.commission = 0.0
        self.currency = ''
        self.realized_pnl = 0.0
        self.yield_value = 0.0
        self.yield_redemption_date = 0

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- CommissionReport to compare to this CommissionReport

        """
        return self.exec_id < other.exec_id
