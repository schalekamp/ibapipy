"""Represents an order.

Unlike the Order class in the native TWSAPI, this merges the information
contained inside the corresponding OrderState class.

"""
import ibapipy.config as config


class Order:
    """Represents an order.

    Attributes not specified in the constructor:
    order_id  --
    client_id --
    perm_id   --
    ...

    """

    def __init__(self, action='', total_quantity=0, order_type='mkt',
                 lmt_price=0.0, aux_price=0.0):
        """Initialize a new instance of a Order.

        Keyword arguments:
        action         -- action to take, either 'buy' or 'sell'
                          (default: '')
        total_quantity -- order quantity in units or shares
                          (default: 0)
        order_type     -- order type ('mkt', 'lmt', 'stp', ...)
                          (default: 'mkt')
        lmt_price      -- limit price for limit orders (default: 0.0)
        aux_price      -- stop price for stop orders (default: 0.0)

        """
        # Main order fields
        self.order_id = 0
        self.client_id = 0
        self.perm_id = 0
        self.action = action
        self.total_quantity = total_quantity
        self.order_type = order_type
        self.lmt_price = lmt_price
        self.aux_price = aux_price
        # State
        self.status = ''
        self.init_margin = ''
        self.maint_margin = ''
        self.equity_with_loan = ''
        self.commission = 0.0
        self.min_commission = 0.0
        self.max_commission = 0.0
        self.commission_currency = ''
        self.warning_text = ''
        # Status fields
        self.filled = 0
        self.remaining = 0
        self.avg_fill_price = 0.0
        self.last_filled_price = 0.0
        self.why_held = ''
        # Extended order fields
        self.tif = ''
        self.oca_group = ''
        self.oca_type = 1
        self.order_ref = ''
        self.transmit = True
        self.parent_id = 0
        self.block_order = False
        self.sweep_to_fill = False
        self.display_size = 0
        self.trigger_method = 0
        self.outside_rth = False
        self.hidden = False
        self.good_after_time = ''
        self.good_till_date = ''
        self.override_percentage_constraints = False
        self.rule_80a = ''
        self.all_or_none = False
        self.min_qty = config.JAVA_INT_MAX
        self.percent_offset = config.JAVA_DOUBLE_MAX
        self.trail_stop_price = config.JAVA_DOUBLE_MAX
        # Financial advisors only
        self.fa_group = ''
        self.fa_profile = ''
        self.fa_method = ''
        self.fa_percentage = ''
        # Institutional orders only
        self.open_close = 'O'
        self.origin = 0
        self.short_sale_slot = 0
        self.designated_location = ''
        self.exempt_code = -1
        # SMART routing only
        self.discretionary_amt = 0.0
        self.etrade_only = False
        self.firm_quote_only = False
        self.nbbo_price_cap = config.JAVA_DOUBLE_MAX
        self.opt_out_smart_routing = False
        # BOX or VOL orders only
        self.auction_strategy = 0
        # BOX orders only
        self.starting_price = config.JAVA_DOUBLE_MAX
        self.stock_ref_price = config.JAVA_DOUBLE_MAX
        self.delta = config.JAVA_DOUBLE_MAX
        # Pegged-to-stock and VOL orders only
        self.stock_range_lower = config.JAVA_DOUBLE_MAX
        self.stock_range_upper = config.JAVA_DOUBLE_MAX
        # Volatility orders only
        self.volatility = config.JAVA_DOUBLE_MAX
        self.volatility_type = config.JAVA_INT_MAX
        self.continuous_update = False
        self.reference_price_type = config.JAVA_INT_MAX
        self.delta_neutral_order_type = ''
        self.delta_neutral_aux_price = config.JAVA_DOUBLE_MAX
        self.delta_neutral_con_id = 0
        self.delta_neutral_settling_firm = ''
        self.delta_neutral_clearing_account = ''
        self.delta_neutral_clearing_intent = ''
        # Combo orders only
        self.basis_points = config.JAVA_DOUBLE_MAX
        self.basis_points_type = config.JAVA_INT_MAX
        # Scale orders only
        self.scale_init_level_size = config.JAVA_INT_MAX
        self.scale_subs_level_size = config.JAVA_INT_MAX
        self.scale_price_increment = config.JAVA_DOUBLE_MAX
        # Hedge orders only
        self.hedge_type = ''
        self.hedge_param = ''
        # Clearing information
        self.account = ''
        self.settling_firm = ''
        self.clearing_account = ''
        self.clearing_intent = ''
        # Algo orders only
        self.algo_strategy = ''
        self.algo_params = []
        # What if
        self.what_if = False
        # Not held
        self.not_held = False
        # SMART combo routing
        # (list of ibapi.data.tag_value.TagValue objects)
        self.smart_combo_routing_params = []

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- Order to compare to this Order

        """
        return self.perm_id < other.perm_id
