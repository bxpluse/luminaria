import os
from datetime import datetime
from enum import Enum

from constants import LOGFILE, ROOT_DIR
from database.stream.log_model import LogModel


class LogLevel(Enum):
    FATAL = 5
    ERROR = 4
    WARN = 3
    INFO = 2
    DEBUG = 1


FILE = os.path.join(ROOT_DIR, LOGFILE)


def log_to_file(app_name, message):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")

    with open(FILE, 'a+') as f:
        f.write('{0}: ({1}) {2}{3}'.format(dt_string[:-3], app_name, message, '\n'))


def log(app_name, message, level=LogLevel.INFO):
    try:
        LogModel.log_message(app_name, message, level.value)
    except Exception as exception:
        log_to_file(app_name, 'Logging to file because exception: {0} Message: {1}'.format(str(exception), message))
