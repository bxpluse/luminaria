from common.enums import APP
from apps.baseapp import App


class HealthCheck(App):
    """
        View logs.
    """

    APP_ID = APP.HEALTH_CHECK

    def __init__(self):
        super().__init__()

    def execute(self, command, **kwargs):
        if command == 'tail':
            return {}
