import json
import select
import socket
import logging

from lesson02.config import Config
from lesson02.descriptors.port import Port
from lesson02.meta.metaclasses import ServerMaker


class Server(metaclass=ServerMaker):
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

    def read_message(self, client):
        encoded_response = client.recv(1024)
        json_response = encoded_response.decode('utf-8')
        return json.loads(json_response)

    def send_message(self, client, message):
        return client.send(message)

    def save_users(self, client):
        response = self.read_message(client)
        self.users[response['user']['account_name']] = client

    def remove_users(self, client):
        response = self.read_message(client)

        print(f'Клиент {client.getpeername()} отключился от сервера.')

        self.clients.remove(client)
        self.users[response['user']['account_name']].close()
        del self.users[response['user']['account_name']]

    def run(self):

        self.init_socket()
        while True:

            try:
                CONN, ADDR = self.sock.accept()
            except OSError:
                pass
            else:
                print(f'Получен запрос на соединение от: {ADDR}')
                self.clients.append(CONN)

            recv_data_lst = []
            send_data_lst = []
            err_lst = []

            try:
                if self.clients:
                    recv_data_lst, send_data_lst, err_lst = select.select(self.clients, self.clients, [], 0)
            except OSError:
                pass

            if recv_data_lst:
                for client_with_message in recv_data_lst:
                    try:

                        message = {}
                        response = self.read_message(client_with_message)

                        if 'action' in response and response['action'] == 'presence':
                            # self.save_users(client_with_message)
                            self.users[response['user']['account_name']] = client_with_message
                            message = {'response': 200}
                        elif 'action' in response and response['action'] == 'message':
                            self.messages.append(response)
                        else:
                            message = {'response': 400, 'error': 'Bad Request'}

                        if len(message) > 0:
                            self.send_message(client_with_message, json.dumps(message).encode('utf-8'))
                    except:
                        self.remove_users(client_with_message)

            for message in self.messages:
                try:
                    if message['destination'] in self.users and self.users[message['destination']] in send_data_lst:
                        destination = self.users[message['destination']]
                        self.send_message(destination, json.dumps(message).encode('utf-8'))

                except:
                    self.remove_users(self.users[message['destination']])

            self.messages.clear()


if __name__ == '__main__':
    server = Server()
    server.run()
