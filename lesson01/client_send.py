"""
    Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
    клиент отправляет запрос серверу;
    Функции клиента:
        сформировать presence-сообщение;
        отправить сообщение серверу;
        получить ответ сервера;
        разобрать сообщение сервера;
        параметры командной строки скрипта client.py <addr> [<port>]:
            addr — ip-адрес сервера;
            port — tcp-порт на сервере, по умолчанию 7777.
"""

import argparse
import json
import logging
import sys
import threading
from socket import socket, AF_INET, SOCK_STREAM
import time

from lesson01.decorators import log
from lesson01.log import client_log_config

LOG = logging.getLogger('app.client')


def parse_args():
    """
    Парсер аргументов коммандной строки
    :return: address and post
    """
    PARSER = argparse.ArgumentParser()

    PARSER.add_argument('--a', help='IP-адрес для подключения', default='localhost')
    PARSER.add_argument('--p', help='TCP-порт для подключения', default=7777)

    ARGS = PARSER.parse_args()

    return ARGS.a, int(ARGS.p)


@log
def create_message(action, account_name='Send'):
    """
    Create message for server
    :param action: Action
    :return: Set
    """
    message = input('Введите сообщение для отправки: ')

    return {
        'action': action,
        'message': message,
        'destination': 'Listener',
        'time': time.time(),
        'user': {
            'account_name': account_name
        }
    }


def create_presence(account_name='Send'):
    """
    create_presence
    :param account_name:
    :return:
    """
    return {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': account_name
        }
    }


def receive_message(socs):
    """
    Обработчик сообщений с сервера
    :param socs:
    :return: None
    """
    while True:
        encoded_response = socs.recv(1024)
        json_response = encoded_response.decode('utf-8')
        answer = json.loads(json_response)

        SENDER = answer['user']['account_name']
        MESSAGE = answer['message']
        print(f'Получено сообщение от пользователя {SENDER}:\n{MESSAGE}')


def send_message(socs):
    """
    Отправка сообщений на сервер
    :param socs:
    :return: None
    """
    while True:
        DATA_MSG = create_message('message')
        socs.send(json.dumps(DATA_MSG).encode('utf-8'))


def start():
    IP, PORT = parse_args()

    try:
        SOCS = socket(AF_INET, SOCK_STREAM)
        SOCS.connect((IP, PORT))

        SOCS.send(json.dumps(create_presence()).encode('utf-8'))

        encoded_response = SOCS.recv(1024)
        json_response = encoded_response.decode('utf-8')
        answer = json.loads(json_response)

        LOG.info(f'Установлено соединение с сервером. Ответ сервера: {answer}')

        print(f'Установлено соединение с сервером.')
    except json.JSONDecodeError:
        LOG.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ConnectionRefusedError:
        LOG.error(f'Не удалось подключиться к серверу {IP}:{PORT}')
        sys.exit(1)
    else:

        receiver = threading.Thread(target=receive_message, args=(SOCS,))
        receiver.daemon = True
        receiver.start()

        sender = threading.Thread(target=send_message, args=(SOCS,))
        sender.daemon = True
        sender.start()

        while True:
            time.sleep(1)
            if receiver.is_alive() and sender.is_alive():
                continue
            break


if __name__ == '__main__':
    start()
