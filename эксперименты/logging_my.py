# -*- coding: utf-8 -*-
import logging
import os

first_logger = logging.getLogger('first_log')
log_formatter = logging.Formatter("%(asctime)s  %(message)s\n", datefmt="%d.%m.%y %H:%M:%S")  # формат сообщения
first_logger.setLevel(logging.INFO)  # уровень важности

#logfile = os.path.join(os.path.realpath(self.config.LOG_FILE_PATH), args[0] + '.log')
logfile = 'log_.log'
file_handler = logging.FileHandler(logfile)  # обработчик для вывода в файл
file_handler.setFormatter(log_formatter)  # подключение форматера к обработчику
first_logger.addHandler(file_handler)  # добавление обработчика в регистр

message = '%s%s%s' % (2, 3, 6)
first_logger.info(message) # вуаля