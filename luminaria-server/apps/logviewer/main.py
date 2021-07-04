import os

from apps.baseapp import App
from common.enums import APP
from constants import LOGFILE, ROOT_DIR
from database.dynamic.log_model import LogModel
from database.stream.executed_job_model import ExecutedJobModel


def convert_level(level):
    level_map = {1: 'DEBUG', 2: 'INFO', 3: 'WARN', 4: 'ERROR', 5: 'FATAL'}
    if level not in level_map:
        return 'UNKNOWN'
    return level_map[level]


class LogViewer(App):
    """
        View logs.
    """

    APP_ID = APP.LOG_VIEWER

    def __init__(self):
        super().__init__()
        self.LOG = os.path.join(ROOT_DIR, LOGFILE)

    @staticmethod
    def tail(lines, apps, levels):
        query = LogModel.tail(lines, apps, levels)
        line = ''
        for i in range(len(query) - 1, -1, -1):
            log = query[i]
            m = '{0}: ({1}) [{2}] {3}'.format(log.datetime_created, log.appname, convert_level(log.level), log.message)
            line += m + '\n'
        return {'lines': line}

    @staticmethod
    def tail_jobs(num_lines=100):
        lines = ExecutedJobModel.tail(num_lines)
        return lines

    def execute(self, command, **kwargs):
        if command == 'tail':
            num_lines = kwargs['numLines']
            apps = kwargs.get('apps', ())
            levels = kwargs.get('levels', (1, 2, 3, 4, 5))
            return self.tail(num_lines, apps, levels)
        elif command == 'tailJob':
            return {'lines': self.tail_jobs()}
