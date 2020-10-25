import os
from vars import ROOT_DIR
from constants import LOGFILE
from apps.baseapp import App


class LogViewer(App):
    """
        View logs.
    """

    APP_ID = 'log-viewer'
    BLOCK_SIZE = 1024

    def __init__(self):
        super().__init__()
        self.LOG = os.path.join(ROOT_DIR, LOGFILE)

    def run(self, lines=20):
        with open(self.LOG, 'rb') as f:
            byts = self.tail(f, lines)
        return byts.decode("utf-8")

    def tail(self, f, lines):
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
