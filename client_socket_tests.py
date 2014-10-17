#!/usr/bin/env python3
"""Tests for the ClientSocket class."""
import unittest
from ibapipy.core.client_socket import ClientSocket
from multiprocessing import Queue


TEST_ACCOUNT_NAME = 'DU109588'


class ClientSocketTests(unittest.TestCase):
    """Test cases for the ClientSocket class."""

    def test_constructor(self):
        client = ClientSocket()
        self.assertFalse(client.is_connected)

    def test_connect(self):
        result_queue = Queue()
        class MockClientSocket(ClientSocket):
            def __init__(self):
                ClientSocket.__init__(self)
            def next_valid_id(self, req_id):
                result_queue.put(req_id)
                result_queue.put('next_valid_id')
        client = MockClientSocket()
        self.assertFalse(client.is_connected)
        client.connect()
        self.assertTrue(client.is_connected)
        while True:
            result = result_queue.get()
            self.assertIsNotNone(result)
            if result == 'next_valid_id':
                break
        client.disconnect()

    def test_disconnect(self):
        client = ClientSocket()
        self.assertFalse(client.is_connected)
        client.connect()
        self.assertTrue(client.is_connected)
        client.disconnect()
        self.assertFalse(client.is_connected)

    def test_req_account_updates(self):
        result_queue = Queue()
        class MockClientSocket(ClientSocket):
            def __init__(self):
                ClientSocket.__init__(self)
            def account_download_end(self, account_name):
                result_queue.put(account_name)
                result_queue.put('account_download_end')
            def update_account_time(self, timestamp):
                result_queue.put(timestamp)
            def update_account_value(self, key, value, currency, account_name):
                result_queue.put(key)
                result_queue.put(value)
                result_queue.put(currency)
                result_queue.put(account_name)
        client = MockClientSocket()
        client.connect()
        client.req_account_updates(True, TEST_ACCOUNT_NAME)
        while True:
            result = result_queue.get()
            self.assertIsNotNone(result)
            if result == 'account_download_end':
                break
        client.disconnect()

    def test_req_all_open_orders(self):
        result_queue = Queue()
        class MockClientSocket(ClientSocket):
            def __init__(self):
                ClientSocket.__init__(self)
            def open_order(self, req_id, contract, order):
                result_queue.put(req_id)
                result_queue.put(contract)
                result_queue.put(order)
            def open_order_end(self):
                result_queue.put('open_order_end')
            def order_status(self, req_id, status, filled, remaining,
                             avg_fill_price, perm_id, parent_id,
                             last_fill_price, client_id, why_held):
                result_queue.put(req_id)
                result_queue.put(status)
                result_queue.put(filled)
                result_queue.put(remaining)
                result_queue.put(avg_fill_price)
                result_queue.put(perm_id)
                result_queue.put(parent_id)
                result_queue.put(last_fill_price)
                result_queue.put(client_id)
                result_queue.put(why_held)
        client = MockClientSocket()
        client.connect()
        client.req_all_open_orders()
        while True:
            result = result_queue.get()
            self.assertIsNotNone(result)
            if result == 'open_order_end':
                break
        client.disconnect()


if __name__ == '__main__':
    unittest.main()
