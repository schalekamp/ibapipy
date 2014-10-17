"""Handle socket communications with the broker."""
from multiprocessing import Process, Queue
from ibapipy.ibapipy_error import IBAPIPyError
import select
import socket
import ibapipy.core.reader as reader
import ibapipy.config as config


class NetworkHandler:

    def __init__(self):
        """Initialize a new instance of a NetworkHandler."""
        self.socket_in_queue = None
        self.socket_out_queue = None
        self.message_queue = Queue()
        self.socket = None
        self.incoming_process = None

    def connect(self, host, port, client_id):
        """Connect to the remote TWS and return the server version and TWS
        connection time.

        Keyword arguments:
        host      -- host name or IP address of the TWS machine
        port      -- port number on the TWS machine
        client_id -- number used to identify this client connection

        """
        if self.socket is not None:
            return 0, 0
        # Connect
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.connect((host, port))
        # Initial handshake
        send(self.socket, config.CLIENT_VERSION)
        response = decode(self.socket.recv(config.BUFFER_SIZE))[0]
        server_version = int(response[0])
        if server_version < config.MIN_SERVER_VERSION:
            msg = 'Server version is {0} (min {1} needed).'
            raise IBAPIPyError(msg.format(server_version,
                                          config.MIN_SERVER_VERSION))
        tws_connection_time = response[1]
        send(self.socket, client_id)
        # Start the outoing request listener
        self.socket_out_queue = Queue()
        process = Process(target=outgoing_listener,
                          args=(self.socket, self.socket_out_queue))
        process.start()
        # Start the incoming socket data --> incoming queue listener
        self.socket_in_queue = Queue()
        process = Process(target=incoming_listener,
                          args=(self.socket, self.socket_in_queue))
        self.incoming_process = process
        self.incoming_process.start()
        # Start the incoming data --> message listener
        process = Process(target=reader.message_listener,
                          args=(self.socket_in_queue, self.message_queue))
        process.start()
        return server_version, tws_connection_time

    def disconnect(self):
        """Disconnect from the remote TWS."""
        if self.socket is None:
            return
        self.socket.shutdown(socket.SHUT_WR)
        self.socket_out_queue.put('stop')
        self.socket_in_queue.put('-1')
        self.message_queue.put(('stop', None))
        self.socket.close()
        self.socket = None


def incoming_listener(in_socket, in_queue):
    data_buffer = b''
    while True:
        try:
            inputready, outputready, exceptrdy = select.select(
                [in_socket], [], [], config.TIMEOUT)
        except select.error as ex:
            # If we close the socket on the client end, select will see a bad
            # file descriptor (the closed socket) and raise an exception with
            # ID 9 (bad file descriptor)
            if ex.args[0] == 9:
                return
            else:
                raise IBAPIPyError('select error', ex)
        for item in inputready:
            raw_data = in_socket.recv(config.BUFFER_SIZE)
            data_buffer += raw_data
            # No more data, go ahead and shut down
            if len(raw_data) == 0:
                in_socket.close()
                return
            else:
                data, remainder = decode(data_buffer)
                data_buffer = remainder
                for item in data:
                    in_queue.put(item, block=False)


def decode(item):
    """Decode the specified item into a list of strings along with a remainder
    made up of extra data.

    The input is expected to be a string of fields separated by the hexadecimal
    value EOL. If 'item' does not end with hex value EOL, it is assumed to be
    incomplete and the last field is returned as 'remainder'.

    If 'item' does end with a terminating hex value of EOL, remainder is the
    empty string.

    Keyword arguments:
    item -- string of fields separated by hex value EOL.

    """
    item = item.decode('utf-8')
    fields = item.split(config.EOL)
    remainder = fields.pop()
    return fields, remainder.encode('utf-8')


def encode(item):
    """Encode the specified item for transmission over the network.

    Item can be of any type, but the encoding will likely not yield predictable
    results for items that are not numeric or string types.

    If item is None, then only the terminating hex value of EOL will be
    returned.

    Keyword arguments:
    item -- item to encode

    """
    if item is None:
        return config.EOL.encode('utf-8')
    item = str(item)
    if item == 'True':
        item = 1
    elif item == 'False':
        item = 0
    result = '%s%s' % (item, config.EOL)
    return result.encode('utf-8')


def outgoing_listener(out_socket, out_queue):
    while True:
        item = out_queue.get()
        if item == 'stop':
            return
        send(out_socket, item)


def send(out_socket, *args):
    """Encode the specified parameter(s) and send over out_socket.

    Keyword arguments:
    out_socket -- outgoing socket
    *args      -- items to send over the network

    """
    for item in args:
        out_socket.sendall(encode(item))
