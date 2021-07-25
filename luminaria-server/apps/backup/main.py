import os
from datetime import date, datetime

from apps.baseapp import App
from common.enums import APP
from constants import DATABASE_CONFIG_NAME, DATABASE_DYNAMIC_NAME, ROOT_DIR


class BackupDatabase(App):
    APP_ID = APP.DB_BACKUP

    def __init__(self):
        super().__init__()

    @staticmethod
    def get_copy_name(db_name):
        cur_time = str(date.today()) + '_' + str(datetime.now().strftime("%H-%M"))
        return 'db_{0}_{1}.sqlite3'.format(db_name, cur_time)

    def blob(self, command, **kwargs):
        if command == 'download':
            db_name = kwargs['dbName']
            file_name = 'db_{0}.sqlite3'.format(db_name)
            return os.path.join(ROOT_DIR, file_name)

    def execute(self, command, **kwargs):
        if command == 'file-name':
            db_name = kwargs['dbName']
            return {'filename': self.get_copy_name(db_name)}
