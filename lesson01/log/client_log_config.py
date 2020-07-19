"""
2.  В каждом модуле выполнить настройку соответствующего логгера по следующему алгоритму:

    Создание именованного логгера;
        Сообщения лога должны иметь следующий формат: "<дата-время> <уровеньважности> <имямодуля> <сообщение>";
        Журналирование должно производиться в лог-файл;
        На стороне сервера необходимо настроить ежедневную ротацию лог-файлов.
"""

import logging

logger = logging.getLogger('app.client')

FORMATTER = logging.Formatter('%(asctime)s - %(levelname)s %(name)s %(message)s')

FILE_HANDLER = logging.FileHandler('client.log', encoding='utf-8')
FILE_HANDLER.setFormatter(FORMATTER)

logger.addHandler(FILE_HANDLER)
logger.setLevel(logging.INFO)
