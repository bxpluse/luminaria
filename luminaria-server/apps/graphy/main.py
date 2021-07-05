from apps.baseapp import App
from common.enums import APP


class Graphy(App):
    APP_ID = APP.GRAPHY

    def __init__(self):
        super().__init__()
        # print("graphy init")

    def execute(self, command, **kwargs):
        if command == 'save':
            return {}
