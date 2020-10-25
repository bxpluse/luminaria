from common.enums import APP, COMMAND, APPSTATUS
from database.apps_model import AppsModel
from common.db_util import create_db, db_exists
from apps.updater.main import ExchangeUpdater
from apps.logviewer.main import LogViewer
from apps.backup.main import BackupDatabase
from apps.monitor.main import RCListener
from database.local_config_model import LocalConfigModel

class AppManager:

    def __init__(self, messenger=None):

        if not db_exists():
            create_db()

        self.apps_model = AppsModel()

        self.exchange_updater = ExchangeUpdater()
        self.log_viewer = LogViewer()
        self.db_backup = BackupDatabase()
        self.rc_listener = RCListener(subs=LocalConfigModel.retrieve('SUBREDDITS_TO_MONITOR'), interval=15)

        self.apps = {
            APP.EXCHANGE_UPDATER: self.exchange_updater,
            APP.LOG_VIEWER: self.log_viewer,
            APP.DB_BACKUP: self.db_backup,
            APP.RC_STREAMER: self.rc_listener
        }

        for app in self.apps.values():
            app.messenger = messenger

    def get_all_apps(self):
        res = self.apps_model.get_all_apps()
        for key, value in res.items():
            if key in self.apps:
                res[key]['status'] = self.apps[key].status.value
            else:
                res[key]['status'] = APPSTATUS.UNKNOWN.value
        return res

    def get_app_status(self, app_id):
        return self.apps[APP(app_id)].status.value

    def execute(self, app_id, command, data=None):
        if command == 'run':
            self.apps[APP(app_id)].run(**data)
        return {}
