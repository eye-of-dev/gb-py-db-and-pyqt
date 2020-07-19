import unittest


class TestClient(unittest.TestCase):
    def setUp(self):
        self.message = {'action': 'message', 'message': 'Привет сервер. Как дела?'}

    def test_message_correct(self):
        self.assertIsInstance(self.message, dict)
