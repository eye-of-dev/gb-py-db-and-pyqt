"""
4.  Продолжаем работать над проектом «Мессенджер»:

        a)  Реализовать скрипт, запускающий два клиентских приложения: на чтение чата и
        на запись в него. Уместно использовать модуль subprocess).
        b) Реализовать скрипт, запускающий указанное количество клиентских приложений.
"""
import subprocess
import os

PROCESSES = []


def get_lesson_dir():
    """
    Функция нахождения корневой директории урока
    :return: string Пусть до корневой папки урока
    """
    return os.getcwd()


def get_root_dir():
    """
    Функция нахождения корневой директории для запуска python
    Актуальна только в данном учебном проекте.
    :return: string Путь к корневой папки проекта
    """
    path = os.getcwd()
    path = path.split('/')
    path.pop()

    return '/'.join(path)


def get_python_script():
    """
    Получить путь до интерпритатора python
    :return: string Пусть до интерпритатора python
    """
    return f'{get_root_dir()}/venv/bin/python'


def get_server_script():
    """
    Получить пусть до скрипта запуска сервера
    :return: string Путь до скрипта запуска сервера
    """
    return f'{get_lesson_dir()}/server.py'


def get_client_send_script():
    """
    Получить пусть до скрипта отправки сообщений
    :return: string Путь до скрипта отправки сообщений
    """
    return f'{get_lesson_dir()}/client_send.py'


def get_client_listener_script():
    """
    Получить пусть до скрипта отправки сообщений
    :return: string Путь до скрипта отправки сообщений
    """
    return f'{get_lesson_dir()}/client_listener.py'


def launcher():
    PROCESSES = []

    print('Выберите команду для запуска нужного приложения:')
    print('s(1) - запустить сервер')
    print('сs(2) - запустить клиент, который будет отправлять сообщения')
    print('сl(3) - запустить клиент, который будет принимать сообщения')
    print('сs_and_cl(4) - запустить оба клиента')
    print('s_and_сs_and_cl(5) - запустить сервер и оба клиента')
    print('exit(6) - выйти из программы')

    while True:

        CODE = input('Введите символьный или числовой код команды: ')

        if CODE in ['s', '1']:
            # Запуск сервера

            PROCESSES.append(subprocess.Popen(f'{get_python_script()} {get_server_script()} --p=9001', shell=True))
        elif CODE in ['сs', '2']:
            # Запуск клиента, который будет отправлять сообщения

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_send_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))
        elif CODE in ['сl', '3']:
            # Запуск клиента, который будет принимать сообщения

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_listener_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))
        elif CODE in ['сs_and_cl', '4']:
            # Запуск обоих клиентов

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_send_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_listener_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))
        elif CODE in ['s_and_сs_and_cl', '5']:
            # Запуск сервера и обоих клиентов

            PROCESSES.append(subprocess.Popen(f'{get_python_script()} {get_server_script()} --p=9001', shell=True))

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_send_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))

            PROCESSES.append(
                subprocess.Popen(f'{get_python_script()} {get_client_listener_script()} --a=127.0.0.1 --p=9001',
                                 shell=True))
        elif CODE in ['exit', '6']:
            print('Вы завершили работу программы. Всего доброго!')
            while PROCESSES:
                VICTIM = PROCESSES.pop()
                VICTIM.kill()
            break
        else:
            print('Нераспознанная команда, повторите ввод!')


if __name__ == '__main__':
    launcher()
