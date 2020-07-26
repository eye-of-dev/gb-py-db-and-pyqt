import json
from datetime import datetime
import unittest
from socket import socket, AF_INET, SOCK_STREAM


class TestServer(unittest.TestCase):
    def setUp(self):
        self.data_answ_success = {
            'time': datetime.now().timestamp(),
            'action': 'message',
            'message': 'Привет сервер. Как дела?'
        }

        self.data_answ_error = {
            'time': datetime.now().timestamp(),
            'action': 'error'
        }

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect(('localhost', 7777))

    def tearDown(self):
        self.s.close()

    def test_action_success(self):
        self.s.send(json.dumps(self.data_answ_success).encode('utf-8'))
        data = self.s.recv(1024)
        data_answ = json.loads(data)
        self.assertEqual(200, data_answ['response'])

    def test_action_error(self):
        self.s.send(json.dumps(self.data_answ_error).encode('utf-8'))
        data = self.s.recv(1024)
        data_answ = json.loads(data)
        self.assertEqual(500, data_answ['response'])

    def test_answer_params_response(self):
        self.s.send(json.dumps(self.data_answ_success).encode('utf-8'))
        data = self.s.recv(1024)
        data_answ = json.loads(data)
        self.assertIn('response', data_answ.keys())

    def test_answer_params_time(self):
        self.s.send(json.dumps(self.data_answ_success).encode('utf-8'))
        data = self.s.recv(1024)
        data_answ = json.loads(data)
        self.assertIn('time', data_answ.keys())
