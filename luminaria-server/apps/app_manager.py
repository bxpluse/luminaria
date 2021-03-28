from apps.backup.main import BackupDatabase
from apps.ipolistener.main import IPOListener
from apps.logviewer.main import LogViewer
from apps.monitor.main import RCListener
from apps.news.main import News
from apps.topten.main import TopTen
from apps.updater.main import ExchangeUpdater
from common.cache import hash_tuple
from common.db_util import create_db, db_exists
from common.enums import APP, APPSTATUS
from database.apps_model import AppsModel
from database.link_model import LinkModel
from database.local_config_model import LocalConfigModel


class AppManager:

    def __init__(self):

        if not db_exists():
            create_db()

        self.apps_model = AppsModel()

        self.exchange_updater = ExchangeUpdater()
        self.log_viewer = LogViewer()
        self.db_backup = BackupDatabase()
        self.rc_listener = RCListener(subs=LocalConfigModel.retrieve('SUBREDDITS_TO_MONITOR'), interval=15)
        self.ipo_listener = IPOListener()
        self.top_ten = TopTen()
        self.news = News()

        self.apps = {
            APP.EXCHANGE_UPDATER: self.exchange_updater,
            APP.LOG_VIEWER: self.log_viewer,
            APP.DB_BACKUP: self.db_backup,
            APP.RC_STREAMER: self.rc_listener,
            APP.IPO_LISTENER: self.ipo_listener,
            APP.TOP_TEN: self.top_ten,
            APP.NEWS: self.news
        }

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

            is_link = LinkModel.select_link_by_app_id(app_entry['id']) is not None
            if is_link:
                app_entry['status'] = APPSTATUS.LINK.value
            app_entry['link_to'] = LinkModel.select_link_by_app_id(app_entry['id'])

        return res

    def get_app_status(self, app_id):
        app = self.apps[APP(app_id)]
        base_data = {'status': app.status.value, 'debugging': app.debugging}
        additional_data = app.get_data()
        return {**base_data, **additional_data}

    def get(self, app_id, command):
        app = self.apps[APP(app_id)]
        res = app.get(command)
        return res

    def blob(self, app_id, command):
        app = self.apps[APP(app_id)]
        file_path = app.blob(command)
        return file_path

    def execute(self, app_id, command, data=None):
        app = self.apps[APP(app_id)]

        # Pre-defined routines
        if command == 'run':
            app.run(**data)
            return {}
        elif command == 'debug':
            app.debugging = data['isDebug']
            return {}
        elif command == 'get':
            return app.get_data()

        # Arbitrary commands

        # Return results if it's found in cache
        hash_id = hash_tuple((command, data))

        res = app.try_cache(hash_id)
        if res is not None:
            return res

        # Execute commands and put in cache
        if data is None:
            res = app.execute(command, **{})
        else:
            res = app.execute(command, **data)

        app.store_to_cache(command, data, res)
        return res
