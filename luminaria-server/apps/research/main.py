from apps.baseapp import App
from common.enums import APP


class Research(App):
    APP_ID = APP.RESEARCH

    def __init__(self):
        super().__init__()

    def execute(self, command, **kwargs):
        if command == 'call':
            return {'res': ''}
