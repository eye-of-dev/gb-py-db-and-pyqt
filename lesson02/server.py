import socket
import logging

from lesson02.config import Config
from lesson02.descrptrs.port import Port


class Server:
    port = Port()

    def __init__(self):
        self.sock = None
        self.port = Config.get_param('server', 'port')
        self.addr = Config.get_param('server', 'host')

        self.clients = []
        self.messages = []

        self.users = dict()

    def init_socket(self):
        """
        Prepare a socket to listen to connected clients
        :return: None
        """
        logging.info(f'Запущен сервер, порт для подключений: {self.port} , адрес с которого принимаются '
                     f'подключения: {self.addr}. Если адрес не указан, принимаются соединения с любых адресов.')

        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.bind((self.addr, self.port))
        transport.settimeout(0.5)

        self.sock = transport
        self.sock.listen()

    def read_message(self):
        pass

    def send_message(self):
        pass

    def run(self):
        """

        :return:
        """

        self.init_socket()
        while True:
            print(self.port)


if __name__ == '__main__':
    server = Server()
    server.run()
