from apps.backup.main import BackupDatabase
from apps.logviewer.main import LogViewer
from apps.monitor.main import RCListener
from apps.updater.main import ExchangeUpdater
from common.db_util import create_db, db_exists
from common.enums import APP, APPSTATUS
from database.apps_model import AppsModel
from database.local_config_model import LocalConfigModel
from database.link_model import LinkModel


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
            app_entry = res[key]
            try:
                app = APP(key)
                if app in self.apps:
                    app_entry['status'] = self.apps[app].status.value
                else:
                    app_entry['status'] = APPSTATUS.UNKNOWN.value
            except ValueError:
                app_entry['status'] = APPSTATUS.UNKNOWN.value

            app_entry['link_to'] = LinkModel.select_link_by_app_id(app_entry['id'])

        return res

    def get_app_status(self, app_id):
        app = self.apps[APP(app_id)]
        base_data = {'status': app.status.value, 'debugging': app.debugging}
        additional_data = app.get_data()
        return {**base_data, **additional_data}

    def execute(self, app_id, command, data=None):
        app = self.apps[APP(app_id)]
        if command == 'run':
            app.run(**data)
        elif command == 'debug':
            app.debugging = data['isDebug']
        return {}
