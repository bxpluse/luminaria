import praw
from apscheduler.schedulers.background import BackgroundScheduler
from database.comment_frequency_model import CommentFrequencyModel
from apps.monitor.preloader import load_all_symbols, load_blacklist
from common.util import parse_word
from config import CLIENT_ID, CLIENT_SECRET
from apps.baseapp import App
from common.enums import APPSTATUS


class RCListener(App):
    APP_ID = 'rc-streamer'

    def __init__(self, subs, interval):

        super().__init__()
        self.SYMBOLS = load_all_symbols() - load_blacklist()
        self.INTERVAL = interval
        self.COMMENT_FREQUENCY_MODEL = CommentFrequencyModel()
        self.SUBREDDITS = subs
        self.REDDIT = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  user_agent="Test Script")
        self.data = {}  # key=symbol, value=times_mentioned
        self.show_config()

    def run(self):
        if self.status == APPSTATUS.READY:
            super().start()
            scheduler = BackgroundScheduler()
            scheduler.add_job(self.commit_to_db, trigger='cron', minute='*/15')
            scheduler.start()
            self.stream()
        super().stop()

    def show_config(self):
        self.info('----------------Loading config------------------')
        self.info('  Interval:      ' + str(self.INTERVAL) + ' min')
        self.info('  Symbols:       ' + str(len(self.SYMBOLS)) + ' monitoring')
        self.info('  Subreddits:    ' + str(self.SUBREDDITS))
        self.info('------------------------------------------------')

    def stream(self):
        for comment in self.REDDIT.subreddit(self.SUBREDDITS).stream.comments(skip_existing=True):
            words = comment.body.split()
            seen_symbols = set()
            for word in words:
                word = parse_word(word)
                if word in self.SYMBOLS and word not in seen_symbols:
                    seen_symbols.add(word)
                    if word not in self.data:
                        self.data[word] = 0
                    self.data[word] += 1

    def commit_to_db(self):
        if len(self.data) > 0:
            self.COMMENT_FREQUENCY_MODEL.insert_interval(**self.data)
            self.data.clear()
