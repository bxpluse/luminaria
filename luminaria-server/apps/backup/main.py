import os
from shutil import copyfile
from datetime import date, datetime
from constants import BACKUP_DIR
from vars import ROOT_DIR, DATABASE_NAME
from apps.baseapp import App
import time


class BackupDatabase(App):

    APP_ID = 'db-backup'

    def __init__(self):
        super().__init__()
        self.dir_path = os.path.join(ROOT_DIR, BACKUP_DIR)
        os.makedirs(self.dir_path, exist_ok=True)

    def run(self, **kwargs):
        super().start()
        cur_time = str(date.today()) + '_' + str(datetime.now().strftime("%H-%M"))
        file_name = 'sqlbackup' + cur_time + '.sqlite3'
        backup_file = os.path.join(self.dir_path, file_name)
        copyfile(os.path.join(ROOT_DIR, DATABASE_NAME), backup_file)
        time.sleep(60)
        super().stop()
