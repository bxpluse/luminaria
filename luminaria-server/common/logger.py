import os
from datetime import datetime
from enum import Enum

from constants import LOGFILE
from database.log_model import LogModel
from vars import ROOT_DIR


class LogLevel(Enum):
    FATAL = 5
    ERROR = 4
    WARN = 3
    INFO = 2
    DEBUG = 1


FILE = os.path.join(ROOT_DIR, LOGFILE)


def log_to_file(appname, info):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")

    with open(FILE, 'a+') as f:
        f.write('{0}: ({1}) {2}{3}'.format(dt_string[:-3], appname, info, '\n'))


def log(appname, info, level=LogLevel.INFO):
    log_to_file(appname, info)
    LogModel.log_message(appname, info, level.value)
