import json
import os
from datetime import date, datetime

from apps.baseapp import App
from common.enums import APP
from common.logger import LogLevel
from constants import ROOT_DIR
from database.kostore.ko_store import KOStore


class DBUtil(App):
    APP_ID = APP.DB_UTIL

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
        elif command == 'fetch-all-ko-md':
            return {'metadatas': KOStore.get_all_metadata()}
        elif command == 'put-ko-md':
            key = kwargs['key']
            value = kwargs['value']
            try:
                dict_value = json.loads(value)
                KOStore.update_metadata(key, dict_value)
                return {'success': True}
            except json.decoder.JSONDecodeError:
                self.log('KO metadata update failed for key [{0}] value [{1}]'
                         .format(key, value), level=LogLevel.ERROR)
                return {'success': False}
