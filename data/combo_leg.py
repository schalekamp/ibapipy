"""Represents a combination leg."""


class ComboLeg:
    """Represents a combination leg."""

    def __init__(self, con_id=0, ratio=0, action='', exchange='', open_close=0,
                 short_sale_slot=0, designated_location='', exempt_code=-1):
        """Initialize a new instance of a ComboLeg.

        Keyword arguments:
        con_id              --
        ratio               --
        action              --
        exchange            --
        open_close          --
        short_sale_slot     --
        designated_location --
        excempt_code        --

        """
        self.con_id = con_id
        self.ratio = ratio
        self.action = action
        self.exchange = exchange
        self.open_close = open_close
        self.short_sale_slot = short_sale_slot
        self.designated_location = designated_location
        self.exempt_code = exempt_code

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- ComboLeg to compare to this ComboLeg

        """
        return self.con_id < other.con_id
