"""
1.  Написать функцию host_ping(), в которой с помощью утилиты ping будет проверяться доступность сетевых узлов.
    Аргументом функции является список, в котором каждый сетевой узел должен быть представлен именем хоста или
    ip-адресом. В функции необходимо перебирать ip-адреса и проверять их доступность с выводом соответствующего
    сообщения («Узел доступен», «Узел недоступен»). При этом ip-адрес сетевого узла должен создаваться с помощью
    функции ip_address().

2.  Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона. Меняться должен только
    последний октет каждого адреса. По результатам проверки должно выводиться соответствующее сообщение.

3.  Написать функцию host_range_ping_tab(), возможности которой основаны на функции из примера 2.
    Но в данном случае результат должен быть итоговым по всем ip-адресам, представленным в табличном формате
    (использовать модуль tabulate). Таблица должна состоять из двух колонок и выглядеть примерно так:
    Reachable
    10.0.0.1
    10.0.0.2

    Unreachable
    10.0.0.3
    10.0.0.4
"""

import ipaddress
import subprocess

from tabulate import tabulate


def host_ping(vars):
    for args in vars:
        ping = subprocess.Popen(args, stdout=subprocess.PIPE)
        limit = 0
        for line in ping.stdout:
            if limit > 2:
                break

            result = line.decode('utf-8')
            if 'no answer yet' in result:
                print(f'Узел {args[-1]} недоступен')
            else:
                print(f'Узел {args[-1]} доступен')

            limit += 1


VARS = [
    ['ping', '-D', '-O', 'yandex.ru'],
    ['ping', '-D', '-O', 'youtube.com'],
    ['ping', '-D', '-O', str(ipaddress.ip_address('8.8.8.8'))],
    ['ping', '-D', '-O', str(ipaddress.ip_address('192.168.0.72'))]
]


host_ping(VARS)


def host_range_ping(subnet):
    subnet = ipaddress.ip_network(subnet)
    for ip in list(subnet.hosts()):
        args = ['ping', '-O', str(ip)]
        ping = subprocess.Popen(args, stdout=subprocess.PIPE)

        limit = 0
        for line in ping.stdout:
            if limit > 1:
                break

            result = line.decode('utf-8')
            if 'no answer yet' in result:
                print(f'Узел {args[-1]} недоступен')
            else:
                print(f'Узел {args[-1]} доступен')

            limit += 1


host_range_ping('8.8.8.0/28')

def host_range_ping_tab(hosts):
    table = {'Reachable': [], 'Unreachable': []}
    for ip in hosts:
        args = ['ping', '-O', str(ip)]
        ping = subprocess.Popen(args, stdout=subprocess.PIPE)

        limit = 0

        for line in ping.stdout:
            if limit > 1:
                break

            result = line.decode('utf-8')

            if 'no answer yet' in result:
                table['Reachable'].append(ip)
            else:
                table['Unreachable'].append(ip)

            limit += 1

    print(tabulate(table, headers='keys', tablefmt="pipe"))


HOSTS = ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4']

host_range_ping_tab(HOSTS)
