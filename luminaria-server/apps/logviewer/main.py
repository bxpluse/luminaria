import os
from common.enums import APP
from apps.baseapp import App
from constants import LOGFILE
from vars import ROOT_DIR
from database.dynamic.log_model import LogModel


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
    BLOCK_SIZE = 1024

    def __init__(self):
        super().__init__()
        self.LOG = os.path.join(ROOT_DIR, LOGFILE)

    def tail_old(self, lines):

        def d(f, lines):
            total_lines_wanted = lines
            f.seek(0, 2)
            block_end_byte = f.tell()
            lines_to_go = total_lines_wanted
            block_number = -1
            blocks = []
            while lines_to_go > 0 and block_end_byte > 0:
                if block_end_byte - self.BLOCK_SIZE > 0:
                    f.seek(block_number * self.BLOCK_SIZE, 2)
                    blocks.append(f.read(self.BLOCK_SIZE))
                else:
                    f.seek(0, 0)
                    blocks.append(f.read(block_end_byte))
                lines_found = blocks[-1].count(b'\n')
                lines_to_go -= lines_found
                block_end_byte -= self.BLOCK_SIZE
                block_number -= 1
            all_read_text = b''.join(reversed(blocks))
            return b'\n'.join(all_read_text.splitlines()[-total_lines_wanted:])

        with open(self.LOG, 'rb') as file:
            byts = d(file, lines)
        decoded = byts.decode("utf-8")
        return {'lines': decoded}

    def tail(self, lines, apps, levels):
        query = LogModel.tail(lines, apps, levels)
        line = ''
        for i in range(len(query) - 1, -1, -1):
            log = query[i]
            m = '{0}: ({1}) [{2}] {3}'.format(log.datetime_created, log.appname, convert_level(log.level), log.message)
            line += m + '\n'
        return {'lines': line}

    def execute(self, command, **kwargs):
        if command == 'tail':
            num_lines = kwargs['numLines']
            apps = kwargs.get('apps', ())
            levels = kwargs.get('levels', (1, 2, 3, 4, 5))
            return self.tail(num_lines, apps, levels)
