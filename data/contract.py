"""Represents a contract.

This merges the Contract and ContractDetails classes from the Java API into a
single class.

"""


class Contract:
    """Represents a single contract.

    Attributes not specified in the constructor:
    local_symbol -- local exchange symbol
    primary_exch -- listing exchange
    min_tick     -- minimum price tick
    long_name    -- long name of the contract
    industry     -- industry classification
    category     -- industry category
    subcategory  -- industry subcategory
    ...

    """

    def __init__(self, sec_type='', symbol='', currency='', exchange=''):
        """Initialize a new instance of a Contract.

        Keyword arguments:
        sec_type -- security type ('STK', 'CASH', 'OPT', etc.)
        symbol   -- symbol of the underlying asset
        currency -- currency
        exchange -- order destination ('SMART', 'IDEALPRO', etc.)

        """
        # Passed parameters
        self.sec_type = sec_type
        self.symbol = symbol
        self.currency = currency
        self.exchange = exchange
        # Basic contract
        if sec_type.lower() == 'cash':
            self.local_symbol = '%s.%s' % (self.symbol, self.currency)
        else:
            self.local_symbol = self.symbol
        self.con_id = 0
        self.expiry = ''
        self.strike = 0
        self.right = ''
        self.multiplier = ''
        self.primary_exch = ''
        self.include_expired = False
        self.sec_id_type = ''
        self.sec_id = ''
        # Combos
        self.combo_legs_descrip = ''
        self.combo_legs = []
        # Delta neutral
        self.under_comp = None
        self.under_type = None
        #
        # Contract details
        #
        self.market_name = ''
        self.trading_class = ''
        self.min_tick = 0
        self.price_magnifier = ''
        self.order_types = ''
        self.valid_exchanges = ''
        self.under_con_id = 0
        self.long_name = ''
        self.contract_month = ''
        self.industry = ''
        self.category = ''
        self.subcategory = ''
        self.time_zone_id = ''
        self.trading_hours = ''
        self.liquid_hours = ''
        # Bond values
        self.cusip = ''
        self.ratings = ''
        self.desc_append = ''
        self.bond_type = ''
        self.coupon_type = ''
        self.callable = False
        self.putable = False
        self.coupon = 0
        self.convertible = False
        self.maturity = ''
        self.issue_date = ''
        self.next_option_date = ''
        self.next_option_type = ''
        self.next_option_partial = False
        self.notes = ''

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Contract to compare to this Contract

        """
        return self.local_symbol < other.local_symbol
