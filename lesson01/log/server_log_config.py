"""
2.  В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:

    Создание именованного логгера;
        Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
        Журналирование должно производиться в лог-файл;
        На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
"""

import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger('app.server')

FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s %(name)s %(message)s')

FILE_HANDLER = logging.FileHandler('server.log', encoding='utf-8')
FILE_HANDLER.setFormatter(FORMATTER)

ROTATE_HANDLER = TimedRotatingFileHandler('server.log', when='D', interval=1, backupCount=7, encoding='utf-8')

logger.addHandler(FILE_HANDLER)
logger.addHandler(ROTATE_HANDLER)
logger.setLevel(logging.DEBUG)
