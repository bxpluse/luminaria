"""
Logs information to a textfile.
"""

import os
from datetime import datetime

from constants import LOGFILE
from vars import ROOT_DIR

FILE = os.path.join(ROOT_DIR, LOGFILE)


def log(appname, info):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S.%f")

    with open(FILE, 'a+') as f:
        f.write('{0}: ({1}) {2}{3}'.format(dt_string[:-3], appname, info, '\n'))
