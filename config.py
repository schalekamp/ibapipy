"""Settings and options for the Interactive Brokers API Python package."""


# *****************************************************************************
# GENERAL OPTIONS
# *****************************************************************************

# End of line code
EOL = '\x00'

# Maximum value of a Java Integer
JAVA_INT_MAX = 2 ** 31 - 1

# Maximum value of a Java Double
JAVA_DOUBLE_MAX = (2 - 2 ** -52) * 2 ** 1023


# *****************************************************************************
# NETWORKING OPTIONS
# *****************************************************************************

# Host name or IP address of the TWS machine
HOST = '127.0.0.1'

# Port number on the TWS machine
PORT = 4001

# Number used to identify a client connection
CLIENT_ID = 0

# Network timeout
TIMEOUT = 60

# Network buffer size
BUFFER_SIZE = 4096


# *****************************************************************************
# CONSTANTS FROM THE EClientSocket JAVA CLASS
# *****************************************************************************

# Version of this client
CLIENT_VERSION = 60

# Minimum supported server version. To reduce code complexity, the myriad
# version checks present in the Java source have been removed. Instead, we
# look for the largest number in the MIN_SERVER_VER_* constants and use that
# value here.
MIN_SERVER_VERSION = 66

# Bag security type
BAG_SEC_TYPE = 'BAG'

# Outoing message IDs
REQ_MKT_DATA = 1
CANCEL_MKT_DATA = 2
PLACE_ORDER = 3
CANCEL_ORDER = 4
REQ_OPEN_ORDERS = 5
REQ_ACCOUNT_DATA = 6
REQ_EXECUTIONS = 7
REQ_IDS = 8
REQ_CONTRACT_DATA = 9
REQ_MKT_DEPTH = 10
CANCEL_MKT_DEPTH = 11
REQ_NEWS_BULLETINS = 12
CANCEL_NEWS_BULLETINS = 13
SET_SERVER_LOGLEVEL = 14
REQ_AUTO_OPEN_ORDERS = 15
REQ_ALL_OPEN_ORDERS = 16
REQ_MANAGED_ACCTS = 17
REQ_FA = 18
REPLACE_FA = 19
REQ_HISTORICAL_DATA = 20
EXERCISE_OPTIONS = 21
REQ_SCANNER_SUBSCRIPTION = 22
CANCEL_SCANNER_SUBSCRIPTION = 23
REQ_SCANNER_PARAMETERS = 24
CANCEL_HISTORICAL_DATA = 25
REQ_CURRENT_TIME = 49
REQ_REAL_TIME_BARS = 50
CANCEL_REAL_TIME_BARS = 51
REQ_FUNDAMENTAL_DATA = 52
CANCEL_FUNDAMENTAL_DATA = 53
REQ_CALC_IMPLIED_VOLAT = 54
REQ_CALC_OPTION_PRICE = 55
CANCEL_CALC_IMPLIED_VOLAT = 56
CANCEL_CALC_OPTION_PRICE = 57
REQ_GLOBAL_CANCEL = 58
REQ_MARKET_DATA_TYPE = 59


# *****************************************************************************
# CONSTANTS FROM THE EReader JAVA CLASS
# *****************************************************************************

# Incoming message IDs
TICK_PRICE = 1
TICK_SIZE = 2
ORDER_STATUS = 3
ERR_MSG = 4
OPEN_ORDER = 5
ACCT_VALUE = 6
PORTFOLIO_VALUE = 7
ACCT_UPDATE_TIME = 8
NEXT_VALID_ID = 9
CONTRACT_DATA = 10
EXECUTION_DATA = 11
MARKET_DEPTH = 12
MARKET_DEPTH_L2 = 13
NEWS_BULLETINS = 14
MANAGED_ACCTS = 15
RECEIVE_FA = 16
HISTORICAL_DATA = 17
BOND_CONTRACT_DATA = 18
SCANNER_PARAMETERS = 19
SCANNER_DATA = 20
TICK_OPTION_COMPUTATION = 21
TICK_GENERIC = 45
TICK_STRING = 46
TICK_EFP = 47
CURRENT_TIME = 49
REAL_TIME_BARS = 50
FUNDAMENTAL_DATA = 51
CONTRACT_DATA_END = 52
OPEN_ORDER_END = 53
ACCT_DOWNLOAD_END = 54
EXECUTION_DATA_END = 55
DELTA_NEUTRAL_VALIDATION = 56
TICK_SNAPSHOT_END = 57
MARKET_DATA_TYPE = 58
COMMISSION_REPORT = 59
