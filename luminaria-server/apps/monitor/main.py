import json
import os
import threading
from common.enums import APP
import praw
from apscheduler.schedulers.background import BackgroundScheduler

from apps.baseapp import App
from common.symbols import load_symbols, load_blacklist, load_whitelist
from common.enums import APPSTATUS
from common.enums import APPTYPE
from common.util import parse_word
from config import CLIENT_ID, CLIENT_SECRET
from config import SCHEDULER_TIME_ZONE
from constants import STATIC_DIR
from vars import ROOT_DIR
from database.comment_frequency_model import CommentFrequencyModel


class RCListener(App):
    APP_ID = APP.RC_STREAMER
    DUMP_FILE = 'dump.json'

    def __init__(self, subs, interval):

        super().__init__(app_type=APPTYPE.STREAMING)
        self.SYMBOLS = set()
        self.INTERVAL = interval
        self.COMMENT_FREQUENCY_MODEL = CommentFrequencyModel()
        self.SUBREDDITS = subs
        self.REDDIT = praw.Reddit(client_id=CLIENT_ID,
                                  client_secret=CLIENT_SECRET,
                                  user_agent="Test Script")
        self.data = {}  # key=symbol, value=times_mentioned
        self.restore_from_file()
        self.load_preloader()
        self.scheduler = BackgroundScheduler({'apscheduler.timezone': SCHEDULER_TIME_ZONE})
        self.scheduler.start()
        self.show_config()

    def run(self):
        super().start()
        job = self.scheduler.add_job(self.commit_to_db, trigger='cron', minute='*/' + str(self.INTERVAL))
        if self.first_start:
            self.log('Stream starting up with schedule: ' + str(self.scheduler.get_jobs()))
        try:
            self.stream()
        except Exception as e:
            self.status = APPSTATUS.ERROR
            self.first_start = False
            job.remove()
            self.log("ERROR: " + (repr(e)))
            self.log("Jobs after catching exception: " + str(self.scheduler.get_jobs()))
            self.log("Restarting ...")
            timer = threading.Timer(30, self.run)
            timer.start()

    def show_config(self):
        self.log('\n' + '----------------Loading config------------------' + '\n'
                 + '    Interval:      ' + str(self.INTERVAL) + ' min' + '\n'
                 + '    Num Symbols:   ' + str(len(self.SYMBOLS)) + '\n'
                 + '    Subreddits:    ' + str(self.SUBREDDITS) + '\n'
                 + '------------------------------------------------'
                 )

    def stream(self):
        self.log('Stream online')
        for comment in self.REDDIT.subreddit(self.SUBREDDITS).stream.comments(skip_existing=True):
            words = comment.body.split()
            seen_symbols = set()
            for word in words:
                if len(word) > 10:
                    continue
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

    def get_data(self):
        next_run = ''
        if len(self.scheduler.get_jobs()) == 1:
            next_run = self.scheduler.get_jobs()[0].next_run_time
        return {'ram': self.data, 'next_run': str(next_run)}

    def restore_from_file(self):
        file_path = os.path.join(ROOT_DIR, STATIC_DIR, self.DUMP_FILE)
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data = json.load(f)
                self.data = data
            os.remove(file_path)

    def dump_to_file(self):
        s = json.dumps(self.data)
        file_path = os.path.join(ROOT_DIR, STATIC_DIR, self.DUMP_FILE)
        with open(file_path, 'w+') as f:
            f.write(s)

    def load_preloader(self):
        self.SYMBOLS = (load_symbols() - load_blacklist()) | load_whitelist()

    def execute(self, command, **kwargs):
        if command == 'reload-symbols':
            self.load_preloader()
        elif command == 'dump-to-file':
            self.dump_to_file()
        return {}
