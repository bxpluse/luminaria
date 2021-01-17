import threading

import praw

from apps.baseapp import App
from apps.monitor.preloader import load_all_symbols, load_blacklist
from common.enums import APPSTATUS
from common.enums import APPTYPE
from common.util import parse_word
from config import CLIENT_ID, CLIENT_SECRET
from database.comment_frequency_model import CommentFrequencyModel


class RCListener(App):
    APP_ID = 'rc-streamer'

    def __init__(self, subs, interval):

        super().__init__(app_type=APPTYPE.STREAMING)
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
        super().start()
        job = self.scheduler.add_job(self.commit_to_db, trigger='cron', minute='*/' + str(self.INTERVAL))
        if self.first_start:
            self.info('Stream starting up with schedule: ' + str(self.scheduler.get_jobs()))
        try:
            self.stream()
        except Exception as e:
            self.status = APPSTATUS.ERROR
            self.first_start = False
            job.remove()
            self.info("ERROR: " + (repr(e)))
            self.info("Jobs after catching exception: " + str(self.scheduler.get_jobs()))
            self.info("Restarting ...")
            timer = threading.Timer(60, self.run)
            timer.start()

    def show_config(self):
        self.info('----------------Loading config------------------')
        self.info('  Interval:      ' + str(self.INTERVAL) + ' min')
        self.info('  Symbols:       ' + str(len(self.SYMBOLS)) + ' monitoring')
        self.info('  Subreddits:    ' + str(self.SUBREDDITS))
        self.info('------------------------------------------------')

    def stream(self):
        self.info('Stream online')
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
        self.debug('committing rows: ' + str(len(self.data)))
        if len(self.data) > 0:
            self.COMMENT_FREQUENCY_MODEL.insert_interval(**self.data)
            self.data.clear()

    def get_data(self):
        next_run = ''
        if len(self.scheduler.get_jobs()) == 1:
            next_run = self.scheduler.get_jobs()[0].next_run_time
        return {'ram': self.data, 'next_run': str(next_run)}

    def load_preloader(self):
        self.SYMBOLS = load_all_symbols() - load_blacklist()

    def execute(self, command, **kwargs):
        if command == 'reload_symbols':
            self.load_preloader()
