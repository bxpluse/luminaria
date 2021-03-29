from apps.baseapp import App
from common.enums import APP


class WordCloud(App):
    """
        Updates CSV file of exchanges.
    """

    APP_ID = APP.TBD

    def __init__(self):
        super().__init__()

    def run(self):
        super().start()


wc = WordCloud()
wc.run()
