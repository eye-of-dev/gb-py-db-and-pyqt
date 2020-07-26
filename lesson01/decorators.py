"""
1.  Продолжая задачу логирования, реализовать декоратор @log, фиксирующий обращение к декорируемой функции.
    Он сохраняет ее имя и аргументы.
2.  В декораторе @log реализовать фиксацию функции, из которой была вызвана декорированная. Если имеется такой код:

        @log
        def func_z():
         pass

        def main():
         func_z()

        ...в логе должна быть отражена информация:
        "<дата-время> Функция func_z() вызвана из функции main"
"""
import inspect
import logging

from lesson01.log import client_log_config

LOG = logging.getLogger('app.client')


def log(func):
    """
    Logging decorator
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper function
        :return:
        """

        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__.split('/')

        LOG.info(f'filename: {filename.pop()} func name: {func.__name__} and func args: {args}, {kwargs}')
        return func(*args, **kwargs)

    return wrapper
