from apps.baseapp import App
from common.cache import Cache
from common.enums import APP
from dataanalysis.sentiment import plot_freq


class Graphy(App):
    APP_ID = APP.GRAPHY

    def __init__(self):
        cache = Cache(60)
        super().__init__(cache=cache)

    def execute(self, command, **kwargs):
        if command == 'getMentionsGraph':
            symbol = kwargs.get('symbol').upper()
            config = kwargs.get('config')
            html = plot_freq(symbol, config=config)
            return {'html': html}
