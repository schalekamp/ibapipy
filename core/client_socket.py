"""Implements the EClientSocket interface for the Interactive Brokers API."""
from ibapipy.core.network_handler import NetworkHandler
import ibapipy.config as config


class ClientSocket:
    """Provides methods for sending requests to TWS."""

    def __init__(self):
        """Initialize a new instance of a ClientSocket."""
        self.network_handler = NetworkHandler()
        self.messages = self.network_handler.message_queue
        self.server_version = 0
        self.tws_connection_time = ''
        self.is_connected = False

    def __send__(self, *args):
        """Hand off each element in args to the NetworkHandler for sending over
        the network.

        *args -- items to send

        """
        for item in args:
            self.network_handler.socket_out_queue.put(item, block=False)

    def cancel_calculate_implied_volatility(self, req_id):
        raise NotImplementedError()

    def calculate_option_price(self, req_id, contract, volatility,
                               under_price):
        raise NotImplementedError()

    def calculate_implied_volatility(self, req_id, contract, price,
                                     under_price):
        raise NotImplementedError()

    def cancel_calculate_option_price(self, req_id):
        raise NotImplementedError()

    def cancel_fundamental_data(self, req_id):
        raise NotImplementedError()

    def cancel_historical_data(self, req_id):
        version = 1
        self.__send__(config.CANCEL_HISTORICAL_DATA, version, req_id)

    def cancel_mkt_data(self, req_id):
        version = 1
        self.__send__(config.CANCEL_MKT_DATA, version, req_id)

    def cancel_mkt_depth(self, req_id):
        raise NotImplementedError()

    def cancel_news_bulletins(self):
        raise NotImplementedError()

    def cancel_order(self, req_id):
        version = 1
        self.__send__(config.CANCEL_ORDER, version, req_id)

    def cancel_real_time_bars(self, req_id):
        raise NotImplementedError()

    def cancel_scanner_subscription(self, req_id):
        raise NotImplementedError()

    def connect(self, host=config.HOST, port=config.PORT,
                client_id=config.CLIENT_ID):
        """Connect to the remote TWS.

        Keyword arguments:
        host      -- host name or IP address of the TWS machine
        port      -- port number on the TWS machine
        client_id -- number used to identify this client connection

        """
        results = self.network_handler.connect(host, port, client_id)
        self.server_version, self.tws_connection_time = results
        self.is_connected = True

    def disconnect(self):
        """Disconnect from the remote TWS."""
        self.network_handler.disconnect()
        self.is_connected = False
        self.server_version = 0
        self.tws_connection_time = ''

    def exercise_options(self, req_id, contract, action, quantity, account,
                         override):
        raise NotImplementedError()

    def place_order(self, req_id, contract, order):
        version = 35
        # Intro and request ID
        self.__send__(config.PLACE_ORDER, version, req_id)
        # Contract fields
        self.__send__(contract.con_id, contract.symbol, contract.sec_type,
                      contract.expiry, contract.strike, contract.right,
                      contract.multiplier, contract.exchange,
                      contract.primary_exch, contract.currency,
                      contract.local_symbol, contract.sec_id_type,
                      contract.sec_id)
        # Main order fields
        self.__send__(order.action, order.total_quantity, order.order_type,
                      order.lmt_price, order.aux_price)
        # Extended order fields
        self.__send__(order.tif, order.oca_group, order.account,
                      order.open_close, order.origin, order.order_ref,
                      order.transmit, order.parent_id, order.block_order,
                      order.sweep_to_fill, order.display_size,
                      order.trigger_method, order.outside_rth, order.hidden)
        # Send combo legs for bag requests
        if config.BAG_SEC_TYPE == contract.sec_type.upper():
            raise NotImplementedError('Bag type not supported yet.')
        self.__send__('')      # deprecated shares_allocation field
        # Everything else (broken into quasi-readble chunks)
        self.__send__(order.discretionary_amt, order.good_after_time,
                      order.good_till_date, order.fa_group, order.fa_method,
                      order.fa_percentage, order.fa_profile,
                      order.short_sale_slot, order.designated_location)
        self.__send__(order.exempt_code, order.oca_type, order.rule_80a,
                      order.settling_firm, order.all_or_none,
                      check(order.min_qty), check(order.percent_offset),
                      order.etrade_only, order.firm_quote_only,
                      check(order.nbbo_price_cap))
        self.__send__(check(order.auction_strategy),
                      check(order.starting_price),
                      check(order.stock_ref_price), check(order.delta),
                      check(order.stock_range_lower),
                      check(order.stock_range_upper),
                      order.override_percentage_constraints,
                      check(order.volatility), check(order.volatility_type),
                      order.delta_neutral_order_type,
                      check(order.delta_neutral_aux_price))
        if len(order.delta_neutral_order_type) > 0:
            self.__send__(order.delta_neutral_con_id,
                          order.delta_neutral_settling_firm,
                          order.delta_neutral_clearing_account,
                          order.delta_neutral_clearing_intent)
        self.__send__(order.continuous_update,
                      check(order.reference_price_type),
                      check(order.trail_stop_price),
                      check(order.scale_init_level_size),
                      check(order.scale_subs_level_size),
                      check(order.scale_price_increment), order.hedge_type)
        if len(order.hedge_type) > 0:
            self.__send__(order.hedge_param)
        self.__send__(order.opt_out_smart_routing, order.clearing_account,
                      order.clearing_intent, order.not_held)
        if contract.under_comp is not None:
            raise NotImplementedError('Under comp not supported yet.')
        else:
            self.__send__(False)
        self.__send__(order.algo_strategy)
        if len(order.algo_strategy) > 0:
            raise NotImplementedError('Algo strategy not supported yet.')
        self.__send__(order.what_if)

    def replace_fa(self, fa_data_type, xml):
        raise NotImplementedError()

    def req_account_updates(self, subscribe, acct_code):
        version = 2
        self.__send__(config.REQ_ACCOUNT_DATA, version, subscribe, acct_code)

    def req_all_open_orders(self):
        version = 1
        self.__send__(config.REQ_ALL_OPEN_ORDERS, version)

    def req_auto_open_orders(self, auto_bind):
        version = 1
        self.__send__(config.REQ_AUTO_OPEN_ORDERS, version, auto_bind)

    def req_contract_details(self, req_id, contract):
        version = 6
        # Contract data message
        self.__send__(config.REQ_CONTRACT_DATA, version, req_id)
        # Contract fields
        self.__send__(contract.con_id, contract.symbol, contract.sec_type,
                      contract.expiry, contract.strike, contract.right,
                      contract.multiplier, contract.exchange,
                      contract.currency, contract.local_symbol,
                      contract.include_expired, contract.sec_id_type,
                      contract.sec_id)

    def req_current_time(self):
        """Returns the current system time on the server side via the
        current_time() wrapper method.

        """
        version = 1
        self.__send__(config.REQ_CURRENT_TIME, version)

    def req_executions(self, req_id, exec_filter):
        version = 3
        # Execution message
        self.__send__(config.REQ_EXECUTIONS, version, req_id)
        # Execution report filter
        self.__send__(exec_filter.client_id, exec_filter.acct_code,
                      exec_filter.time, exec_filter.symbol,
                      exec_filter.sec_type, exec_filter.exchange,
                      exec_filter.side)

    def req_fundamental_data(self, req_id, contract, report_type):
        raise NotImplementedError()

    def req_historical_data(self, req_id, contract, end_date_time,
                            duration_str, bar_size_setting, what_to_show,
                            use_rth, format_date):
        version = 4
        self.__send__(config.REQ_HISTORICAL_DATA, version, req_id)
        # Contract fields
        self.__send__(contract.symbol, contract.sec_type, contract.expiry,
                      contract.strike, contract.right, contract.multiplier,
                      contract.exchange, contract.primary_exch,
                      contract.currency, contract.local_symbol,
                      contract.include_expired)
        # Other stuff
        self.__send__(end_date_time, bar_size_setting, duration_str, use_rth,
                      what_to_show, format_date)
        # Combo legs for bag requests
        if config.BAG_SEC_TYPE == contract.sec_type.upper():
            raise NotImplementedError('Bag type not supported yet.')

    def req_ids(self, num_ids):
        version = 1
        self.__send__(config.REQ_IDS, version, num_ids)

    def req_managed_accts(self):
        version = 1
        self.__send__(config.REQ_MANAGED_ACCTS, version)

    def req_market_data_type(self, type):
        raise NotImplementedError()

    def req_mkt_data(self, req_id, contract, generic_ticklist='',
                     snapshot=False):
        """Return market data via the tick_price(), tick_size(),
        tick_option_computation(), tick_generic(), tick_string() and
        tick_EFP() wrapper methods.

        Keyword arguments:
        req_id           -- unique request ID
        contract         -- ibapi.contract.Contract object
        generic_ticklist -- comma delimited list of generic tick types
                            (default: '')
        snapshot         -- True to return a single snapshot of market data
                            and have the market data subscription cancel;
                            False, otherwise (default: False)

        """
        version = 9
        # Intro and request ID
        self.__send__(config.REQ_MKT_DATA, version, req_id)
        # Contract fields
        self.__send__(contract.con_id, contract.symbol, contract.sec_type,
                      contract.expiry, contract.strike, contract.right,
                      contract.multiplier, contract.exchange,
                      contract.primary_exch, contract.currency,
                      contract.local_symbol)
        if config.BAG_SEC_TYPE == contract.sec_type:
            raise NotImplementedError('Bag type not supported yet.')
        if contract.under_type is not None:
            raise NotImplementedError('Under comp not supported yet.')
        else:
            self.__send__(False)
        # Remaining parameters
        self.__send__(generic_ticklist, snapshot)

    def req_mkt_depth(self, req_id, contract, num_rows):
        raise NotImplementedError()

    def req_news_bulletins(self, all_msgs):
        raise NotImplementedError()

    def req_open_orders(self):
        version = 1
        self.__send__(config.REQ_OPEN_ORDERS, version)

    def req_real_time_bars(self, req_id, contract, bar_size, what_to_show,
                           use_rth):
        raise NotImplementedError()

    def req_scanner_parameters(self):
        raise NotImplementedError()

    def req_scanner_subscription(self, req_id, subscription):
        raise NotImplementedError()

    def request_fa(self, fa_data_type):
        raise NotImplementedError()

    def set_server_log_level(self, log_level=2):
        """Set the logging level of the server.

        Keyword arguments:
        log_level -- level of log entry detail used by the server (TWS)
                     when processing API requests. Valid values include:
                     1 = SYSTEM; 2 = ERROR; 3 = WARNING; 4 = INFORMATION;
                     5 = DETAIL (default: 2)

        """
        version = 1
        self.__send__(config.SET_SERVER_LOGLEVEL, version, log_level)


def check(value):
    """Check to see if the specified value is equal to JAVA_INT_MAX or
    JAVA_DOUBLE_MAX and return None if such is the case; otherwise return
    'value'.

    Interactive Brokers will set certain integers and floats to be their
    maximum possible value in Java.

    This is used as a sentinal value that should be replaced with an EOL when
    transmitting. Here, we check the value and, if it is a max, return None
    which the codec will interpret as an EOL.

    Keyword arguments:
    value -- integer or floating-point value to check

    """
    if is_java_int_max(value) or is_java_double_max(value):
        return None
    else:
        return value


def is_java_double_max(number):
    """Returns True if the specified number is equal to the maximum value of
    a Double in Java; False, otherwise.

    Keyword arguments:
    number -- number to check

    """
    return type(number) == float and number == config.JAVA_DOUBLE_MAX


def is_java_int_max(number):
    """Returns True if the specified number is equal to the maximum value of
    an Integer in Java; False, otherwise.

    Keyword arguments:
    number -- number to check

    """
    return type(number) == int and number == config.JAVA_INT_MAX
