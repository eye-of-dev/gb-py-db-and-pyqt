"""
    Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
    сервер отвечает соответствующим кодом результата.
    Функции сервера:
        принимает сообщение клиента;
        формирует ответ клиенту;
        отправляет ответ клиенту;
        имеет параметры командной строки:
            -p <port> — TCP-порт для работы (по умолчанию использует 7777);
            -a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

import argparse
import json
import logging
import select
from socket import socket, AF_INET, SOCK_STREAM

from lesson01.log import server_log_config

LOG = logging.getLogger('app.server')


def parse_args():
    """
    Парсер аргументов коммандной строки
    :return: address and post
    """
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument('--a', help='IP-адрес для прослушивания', default='')
    PARSER.add_argument('--p', help='TCP-порт для прослушивания', default=7777)

    ARGS = PARSER.parse_args()

    return ARGS.a, int(ARGS.p)


def start():
    """
    Запуск сервера и обработка сообщений
    :return: None
    """
    print('---===Сервер запущен===---')

    IP, PORT = parse_args()

    SOCS = socket(AF_INET, SOCK_STREAM)
    SOCS.bind((IP, PORT))
    SOCS.listen(5)
    SOCS.settimeout(0.2)

    clients = []
    messages = []

    users = dict()

    while True:

        try:
            CONN, ADDR = SOCS.accept()
        except OSError:
            pass
        else:
            LOG.info(f'Получен запрос на соединение от: {ADDR}')
            clients.append(CONN)

        recv_data_lst = []
        send_data_lst = []
        err_lst = []

        try:
            if clients:
                recv_data_lst, send_data_lst, err_lst = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_lst:
            for client_with_message in recv_data_lst:
                try:

                    # @todo вывести в отдельный метод
                    encoded_response = client_with_message.recv(1024)
                    json_response = encoded_response.decode('utf-8')
                    response = json.loads(json_response)

                    if 'action' in response and response['action'] == 'presence':

                        # @todo вывести в отдельный метод
                        users[response['user']['account_name']] = client_with_message
                        client_with_message.send(json.dumps({'response': 200}).encode('utf-8'))

                    elif 'action' in response and response['action'] == 'message':
                        messages.append(response)
                    else:
                        client_with_message.send(json.dumps({'response': 400, 'error': 'Bad Request'}).encode('utf-8'))
                except:

                    # @todo вывести в отдельный метод
                    LOG.info(f'Клиент {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)
                    users[response['user']['account_name']].close()
                    del users[response['user']['account_name']]

        for message in messages:
            try:
                if message['destination'] in users and users[message['destination']] in send_data_lst:
                    # @todo сделать читабельнее
                    users[message['destination']].send(json.dumps(message).encode('utf-8'))
            except:

                # @todo вывести в отдельный метод
                LOG.info(f'Клиент {message["destination"]} отключился от сервера.')
                clients.remove(users[message['destination']])
                del users[message['destination']]

        messages.clear()


if __name__ == '__main__':
    start()

# Пример запуска сервера: server.py --a=127.0.0.1 --p=9001
# ------------------
# Подключился клиент:  ('127.0.0.1', 47034)
# Подключился клиент:  ('127.0.0.1', 47036)
# Подключился клиент:  ('127.0.0.1', 47038)
