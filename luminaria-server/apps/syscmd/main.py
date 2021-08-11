from apps.baseapp import App
from common.enums import APP, Variant
from common.messenger import Toast
from database.config.apps_model import AppsModel


class Syscmd(App):

    APP_ID = APP.SYSCMD

    def __init__(self):
        super().__init__()
        self.online_apps = {}
        self.refresh_apps()

    def refresh_apps(self):
        self.online_apps = AppsModel.get_all_online_apps()

    def execute(self, command, **kwargs):
        if command == 'refresh-apps':
            self.refresh_apps()
            return {'<TOAST>': Toast('Apps Refreshed', duration=2.5, variant=Variant.SUCCESS)}
        if command == 'refresh-config':
            self.configuration.refresh_config_map()
            return {'<TOAST>': Toast('Config Refreshed', duration=2.5, variant=Variant.SUCCESS)}
