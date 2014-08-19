"""Implements a functional version of the EWrapper interface for the
Interactive Brokers API.

Unlike its Java counterpart, this module does not call EReader methods, but
rather puts messages into a queue of the form ('method name', (parm1, ...)).

To reduce code complexity, the myriad version checks present in the Java source
have been removed. Instead, we look for the largest number in each function and
raise a warning if that minimum is not met.

"""
from multiprocessing.queues import Empty
from ibapipy.ibapipy_error import IBAPIPyError
from ibapipy.data.combo_leg import ComboLeg
from ibapipy.data.commission_report import CommissionReport
from ibapipy.data.contract import Contract
from ibapipy.data.execution import Execution
from ibapipy.data.order import Order
from ibapipy.data.order_combo_leg import OrderComboLeg
from ibapipy.data.tag_value import TagValue
from ibapipy.data.under_comp import UnderComp
import calendar
import pytz
import ibapipy.config as config


# Error message for versions.
VERSION_ERROR = 'Version is {0:d} (min {1:d} needed)'


def _str_to_ms(time_str, timezone='UTC', formatting='%Y-%m-%d %H:%M:%S.%f'):
    """Return the time in milliseconds since the Epoch for the specified
    time string.

    Keyword arguments:
    time_str -- time string

    """
    dtime = pytz.datetime.datetime.strptime(time_str, formatting)
    # Note that in order for daylight savings conversions to work, we
    # MUST use localize() here and cannot simply pass a timezone into the
    # datetime constructor. This is because derple, werpy, durp, durp ...
    tzone = pytz.timezone(timezone)
    dtime = pytz.datetime.datetime(dtime.year, dtime.month, dtime.day,
                                   dtime.hour, dtime.minute, dtime.second,
                                   dtime.microsecond)
    dtime = tzone.localize(dtime)
    dtime = dtime.astimezone(pytz.timezone('UTC'))
    milliseconds = calendar.timegm(dtime.utctimetuple()) * 1000
    milliseconds = int(milliseconds + dtime.microsecond / 1000.0)
    return milliseconds


def get_bool(socket_in_queue, timeout=10):
    return bool(get_int(socket_in_queue, timeout=timeout))


def get_int(socket_in_queue, default_max=False, timeout=10):
    item = get_str(socket_in_queue, timeout)
    default = config.JAVA_INT_MAX if default_max else 0
    return default if len(item) == 0 else int(item)


def get_float(socket_in_queue, default_max=False, timeout=10):
    item = get_str(socket_in_queue, timeout)
    default = config.JAVA_DOUBLE_MAX if default_max else 0
    return default if len(item) == 0 else float(item)


def get_str(socket_in_queue, timeout=10):
    return socket_in_queue.get(timeout=timeout).lower()


def message_listener(socket_in_queue, message_queue):
    # Message ID to function mappings.
    message_ids = {config.ACCT_DOWNLOAD_END: account_download_end,
                   config.ACCT_UPDATE_TIME: account_update_time,
                   config.ACCT_VALUE: account_value,
                   config.CONTRACT_DATA: contract_details,
                   config.CONTRACT_DATA_END: contract_details_end,
                   config.CURRENT_TIME: current_time,
                   config.ERR_MSG: error,
                   config.EXECUTION_DATA: exec_details,
                   config.EXECUTION_DATA_END: exec_details_end,
                   config.HISTORICAL_DATA: historical_data,
                   config.MANAGED_ACCTS: managed_accounts,
                   config.NEXT_VALID_ID: next_valid_id,
                   config.OPEN_ORDER: open_order,
                   config.OPEN_ORDER_END: open_order_end,
                   config.ORDER_STATUS: order_status,
                   config.PORTFOLIO_VALUE: portfolio_value,
                   config.TICK_GENERIC: tick_generic,
                   config.TICK_PRICE: tick_price,
                   config.TICK_SIZE: tick_size,
                   config.TICK_STRING: tick_string,
                   config.COMMISSION_REPORT: commission_report}
    while True:
        try:
            message_id = get_int(socket_in_queue)
        except Empty:
            continue
        if message_id in message_ids:
            message_ids[message_id](socket_in_queue, message_queue)
        elif message_id < 0:
            return
        else:
            raise IBAPIPyError('Unsupported message ID: {0}'.format(message_id))


def account_download_end(in_queue, out_queue):
    get_int(in_queue)      # version
    account_name = get_str(in_queue)
    result = ('account_download_end', (account_name,))
    out_queue.put(result, block=False)


def account_update_time(in_queue, out_queue):
    get_int(in_queue)      # version
    timestamp = get_str(in_queue)
    result = ('update_account_time', (timestamp,))
    out_queue.put(result, block=False)


def account_value(in_queue, out_queue):
    get_int(in_queue)      # version
    key = get_str(in_queue)
    value = get_str(in_queue)
    currency = get_str(in_queue)
    account_name = get_str(in_queue)
    result = ('update_account_value', (key, value, currency, account_name))
    out_queue.put(result, block=False)


def commission_report(in_queue, out_queue):
    get_int(in_queue)      # version
    report = CommissionReport()
    report.exec_id = get_str(in_queue)
    report.commission = get_float(in_queue)
    report.currency = get_str(in_queue)
    report.realized_pnl = get_float(in_queue)
    report.yield_value = get_float(in_queue)
    report.yield_redemption_date = get_int(in_queue)
    result = ('commission_report', (report,))
    out_queue.put(result, block=False)


def contract_details(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 8:
        raise IBAPIPyError(VERSION_ERROR.format(version, 8))
    req_id = get_int(in_queue)
    contract = Contract()
    contract.symbol = get_str(in_queue)
    contract.sec_type = get_str(in_queue)
    contract.expiry = get_str(in_queue)
    contract.strike = get_float(in_queue)
    contract.right = get_str(in_queue)
    contract.exchange = get_str(in_queue)
    contract.currency = get_str(in_queue)
    contract.local_symbol = get_str(in_queue)
    contract.market_name = get_str(in_queue)
    contract.trading_class = get_str(in_queue)
    contract.con_id = get_int(in_queue)
    contract.min_tick = get_float(in_queue)
    contract.multiplier = get_str(in_queue)
    contract.order_types = get_str(in_queue)
    contract.valid_exchanges = get_str(in_queue)
    contract.price_magnifier = get_int(in_queue)
    contract.under_con_id = get_int(in_queue)
    contract.long_name = get_str(in_queue)
    contract.primary_exch = get_str(in_queue)
    contract.contract_month = get_str(in_queue)
    contract.industry = get_str(in_queue)
    contract.category = get_str(in_queue)
    contract.subcategory = get_str(in_queue)
    contract.time_zone_id = get_str(in_queue)
    contract.trading_hours = get_str(in_queue)
    contract.liquid_hours = get_str(in_queue)
    contract.ev_rule = get_str(in_queue)
    contract.ev_multiplier = get_float(in_queue)
    sec_id_list_count = get_int(in_queue)
    if sec_id_list_count > 0:
        contract.sec_id_list = []
        tag_value = TagValue()
        tag_value.tag = get_str(in_queue)
        tag_value.value = get_str(in_queue)
        contract.sec_id_list.append(tag_value)
    result = ('contract_details', (req_id, contract))
    out_queue.put(result, block=False)


def contract_details_end(in_queue, out_queue):
    get_int(in_queue)      # version
    req_id = get_int(in_queue)
    result = ('contract_details_end', (req_id,))
    out_queue.put(result, block=False)


def current_time(in_queue, out_queue):
    get_int(in_queue)     # version
    seconds = get_int(in_queue)
    result = ('current_time', (seconds,))
    out_queue.put(result, block=False)


def error(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 2:
        message = get_str(in_queue)
        result = ('error', (0, 0, message))
    else:
        req_id = get_int(in_queue)
        code = get_int(in_queue)
        message = get_str(in_queue)
        result = ('error', (req_id, code, message))
    out_queue.put(result, block=False)


def exec_details(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 9:
        raise IBAPIPyError(VERSION_ERROR.format(version, 9))
    req_id = get_int(in_queue)
    order_id = get_int(in_queue)
    # Contract fields
    contract = Contract()
    contract.con_id = get_int(in_queue)
    contract.symbol = get_str(in_queue)
    contract.sec_type = get_str(in_queue)
    contract.expiry = get_str(in_queue)
    contract.strike = get_float(in_queue)
    contract.right = get_str(in_queue)
    contract.multiplier = get_str(in_queue)
    contract.exchange = get_str(in_queue)
    contract.currency = get_str(in_queue)
    contract.local_symbol = get_str(in_queue)
    # Execution fields
    execution = Execution()
    execution.order_id = order_id
    execution.exec_id = get_str(in_queue)
    execution.time = get_str(in_queue)
    # Milliseconds is not part of the standard IB Execution, but we add it here
    execution.milliseconds = _str_to_ms(execution.time, timezone='UTC',
                                        formatting='%Y%m%d  %H:%M:%S')
    execution.acct_number = get_str(in_queue)
    execution.exchange = get_str(in_queue)
    execution.side = get_str(in_queue)
    execution.shares = get_int(in_queue)
    execution.price = get_float(in_queue)
    execution.perm_id = get_int(in_queue)
    execution.client_id = get_int(in_queue)
    execution.liquidation = get_int(in_queue)
    execution.cum_qty = get_int(in_queue)
    execution.avg_price = get_float(in_queue)
    execution.order_ref = get_str(in_queue)
    execution.ev_rule = get_str(in_queue)
    execution.ev_multiplier = get_float(in_queue)
    result = ('exec_details', (req_id, contract, execution))
    out_queue.put(result, block=False)


def exec_details_end(in_queue, out_queue):
    get_int(in_queue)      # version
    req_id = get_int(in_queue)
    result = ('exec_details_end', (req_id,))
    out_queue.put(result, block=False)


def historical_data(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 3:
        raise IBAPIPyError(VERSION_ERROR.format(version, 3))
    req_id = get_int(in_queue)
    start_date = get_str(in_queue)
    end_date = get_str(in_queue)
    completed_indicator = 'finished-{0}-{1}'.format(start_date, end_date)
    item_count = get_int(in_queue)
    for index in range(item_count):
        date = get_str(in_queue)
        open = get_float(in_queue)
        high = get_float(in_queue)
        low = get_float(in_queue)
        close = get_float(in_queue)
        volume = get_int(in_queue)
        wap = get_float(in_queue)
        has_gaps = get_str(in_queue)
        has_gaps = True if has_gaps == 'true' else 'false'
        bar_count = get_int(in_queue)
        result = ('historical_data', (req_id, date, open, high, low, close,
                                      volume, bar_count, wap, has_gaps))
        out_queue.put(result, block=False)
    result = ('historical_data', (req_id, completed_indicator, -1, -1, -1, -1,
                                  -1, -1, -1, False))
    out_queue.put(result, block=False)


def managed_accounts(in_queue, out_queue):
    get_int(in_queue)     # version
    accounts = get_str(in_queue)
    result = ('managed_accounts', (accounts,))
    out_queue.put(result, block=False)


def next_valid_id(in_queue, out_queue):
    get_int(in_queue)     # version
    req_id = get_int(in_queue)
    result = ('next_valid_id', (req_id,))
    out_queue.put(result, block=False)


def open_order(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 31:
        raise IBAPIPyError(VERSION_ERROR.format(version, 31))
    # Order ID
    order = Order()
    order.order_id = get_int(in_queue)
    # Contract fields
    contract = Contract()
    contract.con_id = get_int(in_queue)
    contract.symbol = get_str(in_queue)
    contract.sec_type = get_str(in_queue)
    contract.expiry = get_str(in_queue)
    contract.strike = get_float(in_queue)
    contract.right = get_str(in_queue)
    contract.exchange = get_str(in_queue)
    contract.currency = get_str(in_queue)
    contract.local_symbol = get_str(in_queue)
    # Order fields
    order.action = get_str(in_queue)
    order.total_quantity = get_int(in_queue)
    order.order_type = get_str(in_queue)
    order.lmt_price = get_float(in_queue)
    order.aux_price = get_float(in_queue)
    order.tif = get_str(in_queue)
    order.oca_group = get_str(in_queue)
    order.account = get_str(in_queue)
    order.open_close = get_str(in_queue)
    order.origin = get_int(in_queue)
    order.order_ref = get_str(in_queue)
    order.client_id = get_int(in_queue)
    order.perm_id = get_int(in_queue)
    order.outside_rth = get_bool(in_queue)
    order.hidden = get_bool(in_queue)
    order.discretionary_amt = get_float(in_queue)
    order.good_after_time = get_str(in_queue)
    get_str(in_queue)     # deprecated shares_allocation field
    order.fa_group = get_str(in_queue)
    order.fa_method = get_str(in_queue)
    order.fa_percentage = get_str(in_queue)
    order.fa_profile = get_str(in_queue)
    order.good_till_date = get_str(in_queue)
    order.rule_80a = get_str(in_queue)
    order.percent_offset = get_float(in_queue)
    order.settling_firm = get_str(in_queue)
    order.short_sale_slot = get_int(in_queue)
    order.designated_location = get_str(in_queue)
    order.exempt_code = get_int(in_queue)
    order.auction_strategy = get_int(in_queue)
    order.starting_price = get_float(in_queue)
    order.stock_ref_price = get_float(in_queue)
    order.delta = get_float(in_queue)
    order.stock_range_lower = get_float(in_queue)
    order.stock_range_upper = get_float(in_queue)
    order.display_size = get_int(in_queue)
    order.block_order = get_bool(in_queue)
    order.sweep_to_fill = get_bool(in_queue)
    order.all_or_none = get_bool(in_queue)
    order.min_qty = get_int(in_queue)
    order.oca_type = get_int(in_queue)
    order.etrade_only = get_bool(in_queue)
    order.firm_quote_only = get_bool(in_queue)
    order.nbbo_price_cap = get_float(in_queue)
    order.parent_id = get_int(in_queue)
    order.trigger_method = get_int(in_queue)
    order.volatility = get_float(in_queue)
    order.volatility_type = get_int(in_queue)
    order.delta_neutral_order_type = get_str(in_queue)
    order.delta_neutral_aux_price = get_float(in_queue)
    if len(order.delta_neutral_order_type) > 0:
        order.delta_neutral_con_id = get_int(in_queue)
        order.delta_neutral_settling_firm = get_str(in_queue)
        order.delta_neutral_clearing_account = get_str(in_queue)
        order.delta_neutral_clearing_intent = get_str(in_queue)
        order.delta_neutral_open_close = get_str(in_queue)
        order.delta_neutral_short_sale = get_bool(in_queue)
        order.delta_neutral_short_sale_slot = get_int(in_queue)
        order.delta_neutral_designation_location = get_str(in_queue)
    order.continuous_update = get_int(in_queue)
    order.reference_price_type = get_int(in_queue)
    order.trail_stop_price = get_float(in_queue, True)
    order.trailing_percent = get_float(in_queue, True)
    order.basis_points = get_float(in_queue)
    order.basis_points_type = get_int(in_queue)
    contract.combo_legs_descrip = get_str(in_queue)
    combo_legs_count = get_int(in_queue)
    if combo_legs_count > 0:
        contract.combo_legs = []
        for index in range(combo_legs_count):
            con_id = get_int(in_queue)
            ratio = get_int(in_queue)
            action = get_str(in_queue)
            exchange = get_str(in_queue)
            open_close = get_int(in_queue)
            short_sale_slot = get_int(in_queue)
            designated_location = get_str(in_queue)
            exempt_code = get_int(in_queue)
            combo_leg = ComboLeg(con_id, ratio, action, exchange, open_close,
                                 short_sale_slot, designated_location,
                                 exempt_code)
            contract.combo_legs.append(combo_leg)
    order_combo_legs_count = get_int(in_queue)
    if order_combo_legs_count > 0:
        order.order_combo_legs = []
        for index in range(order_combo_legs_count):
            price = get_float(in_queue, True)
            order_combo_leg = OrderComboLeg(price)
            order.order_combo_legs.append(order_combo_leg)
    smart_params_count = get_int(in_queue)
    if smart_params_count > 0:
        order.smart_combo_routing_params = []
        for index in range(0, smart_params_count):
            tag_value = TagValue()
            tag_value.tag = get_str(in_queue)
            tag_value.value = get_str(in_queue)
            order.smart_combo_routing_params.append(tag_value)
    order.scale_init_level_size = get_int(in_queue, True)
    order.scale_subs_level_size = get_int(in_queue, True)
    order.scale_price_increment = get_float(in_queue, True)
    if order.scale_price_increment > 0 and \
            order.scale_price_increment < config.JAVA_DOUBLE_MAX:
        order.scale_price_adjust_value = get_float(in_queue, True)
        order.scale_price_adjust_interval = get_int(in_queue, True)
        order.scale_profit_offset = get_float(in_queue, True)
        order.scale_auto_reset = get_bool(in_queue)
        order.scale_init_position = get_int(in_queue, True)
        order.scale_init_fill_qty = get_int(in_queue, True)
        order.scale_random_percent = get_bool(in_queue)
    order.hedge_type = get_str(in_queue)
    if len(order.hedge_type) > 0:
        order.hedge_param = get_str(in_queue)
    order.opt_out_smart_routing = get_bool(in_queue)
    order.clearing_account = get_str(in_queue)
    order.clearing_intent = get_str(in_queue)
    order.not_held = get_bool(in_queue)
    if get_bool(in_queue):
        under_comp = UnderComp()
        under_comp.con_id = get_int(in_queue)
        under_comp.delta = get_float(in_queue)
        under_comp.price = get_float(in_queue)
        contract.under_comp = under_comp
    order.algo_strategy = get_str(in_queue)
    if len(order.algo_strategy) > 0:
        algo_params_count = get_int(in_queue)
        if algo_params_count > 0:
            order.algo_params = []
            for index in range(0, algo_params_count):
                tag_value = TagValue()
                tag_value.tag = get_str(in_queue)
                tag_value.value = get_str(in_queue)
                order.algo_params.append(tag_value)
    order.what_if = get_bool(in_queue)
    # Order state
    order.status = get_str(in_queue)
    order.init_margin = get_str(in_queue)
    order.maint_margin = get_str(in_queue)
    order.equity_with_loan = get_str(in_queue)
    order.commission = get_float(in_queue, True)
    order.min_commission = get_float(in_queue, True)
    order.max_commission = get_float(in_queue, True)
    order.commission_currency = get_str(in_queue)
    order.warning_text = get_str(in_queue)
    result = ('open_order', (order.order_id, contract, order))
    out_queue.put(result, block=False)


def open_order_end(in_queue, out_queue):
    get_int(in_queue)       # version
    result = ('open_order_end', ())
    out_queue.put(result, block=False)


def order_status(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 6:
        raise IBAPIPyError(VERSION_ERROR.format(version, 6))
    req_id = get_int(in_queue)
    status = get_str(in_queue)
    filled = get_int(in_queue)
    remaining = get_int(in_queue)
    avg_fill_price = get_float(in_queue)
    perm_id = get_int(in_queue)
    parent_id = get_int(in_queue)
    last_fill_price = get_float(in_queue)
    client_id = get_int(in_queue)
    why_held = get_str(in_queue)
    result = ('order_status', (req_id, status, filled, remaining,
                               avg_fill_price, perm_id, parent_id,
                               last_fill_price, client_id, why_held))
    out_queue.put(result, block=False)


def portfolio_value(in_queue, out_queue):
    version = get_int(in_queue)
    if version < 7:
        raise IBAPIPyError(VERSION_ERROR.format(version, 7))
    contract = Contract()
    contract.con_id = get_int(in_queue)
    contract.symbol = get_str(in_queue)
    contract.sec_type = get_str(in_queue)
    contract.expiry = get_str(in_queue)
    contract.strike = get_float(in_queue)
    contract.right = get_str(in_queue)
    contract.multiplier = get_str(in_queue)
    contract.primary_exch = get_str(in_queue)
    contract.currency = get_str(in_queue)
    contract.local_symbol = get_str(in_queue)
    position = get_int(in_queue)
    market_price = get_float(in_queue)
    market_value = get_float(in_queue)
    average_cost = get_float(in_queue)
    unrealized_pnl = get_float(in_queue)
    realized_pnl = get_float(in_queue)
    account_name = get_str(in_queue)
    result = ('update_portfolio', (contract, position, market_price,
                                   market_value, average_cost, unrealized_pnl,
                                   realized_pnl, account_name))
    out_queue.put(result, block=False)


def tick_generic(in_queue, out_queue):
    get_int(in_queue)      # version
    req_id = get_int(in_queue)
    tick_type = get_int(in_queue)
    value = get_float(in_queue)
    result = ('tick_generic', (req_id, tick_type, value))
    out_queue.put(result, block=False)


def tick_price(in_queue, out_queue):
    # Tick price
    version = get_int(in_queue)
    if version < 3:
        raise IBAPIPyError(VERSION_ERROR.format(version, 3))
    req_id = get_int(in_queue)
    tick_type = get_int(in_queue)
    price = get_float(in_queue)
    size = get_int(in_queue)
    can_auto_execute = get_int(in_queue)
    result = ('tick_price', (req_id, tick_type, price, can_auto_execute))
    out_queue.put(result, block=False)
    # Tick size
    size_tick_type = -1
    if tick_type == 1:
        size_tick_type = 0
    elif tick_type == 2:
        size_tick_type = 3
    elif tick_type == 4:
        size_tick_type = 5
    if size_tick_type != -1:
        result = ('tick_size', (req_id, size_tick_type, size))
        out_queue.put(result, block=False)


def tick_size(in_queue, out_queue):
    get_int(in_queue)     # version
    req_id = get_int(in_queue)
    tick_type = get_int(in_queue)
    size = get_int(in_queue)
    result = ('tick_size', (req_id, tick_type, size))
    out_queue.put(result, block=False)


def tick_string(in_queue, out_queue):
    get_int(in_queue)     # version
    req_id = get_int(in_queue)
    tick_type = get_int(in_queue)
    value = get_str(in_queue)
    result = ('tick_string', (req_id, tick_type, value))
    out_queue.put(result, block=False)
