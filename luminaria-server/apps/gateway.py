import bcrypt


from database.config.global_config_model import GlobalConfigModel

MASTER_SESSION_ID = GlobalConfigModel.retrieve('SESSION_ID').encode()


def authenticate(func):
    def inner(*args, **kwargs):
        session_id = args[-1].get('session_id', None)

        # Validate session id is present
        if session_id is None:
            return {'error': 'No session id'}, 401

        # Validate session id is correct
        if not bcrypt.checkpw(session_id.encode(), MASTER_SESSION_ID):
            return {'error': 'Session id incorrect'}, 401

        return func(*args, **kwargs)

    return inner


class Gateway:

    def __init__(self, app_manager, messenger):
        self.app_manager = app_manager
        self.messenger = messenger

    @authenticate
    def raw(self, command, data):
        if command == 'get-all-apps':
            return self.app_manager.get_all_apps()
        return {}

    @authenticate
    def blob(self, app_id, command, data):
        return self.app_manager.blob(app_id, command, data)

    @authenticate
    def status(self, app_id, data):
        return self.app_manager.status(app_id)

    @authenticate
    def execute(self, app_id, command, data):
        res = self.app_manager.execute(app_id, command, data)
        if not res:
            return {}
        if '<TOAST>' in res:
            self.messenger.toast(res['<TOAST>'])
            del res['<TOAST>']
        return res

    def query(self, app_id, command, data):
        res = self.app_manager.query(app_id, command, data)
        if not res:
            return {}
        return res
