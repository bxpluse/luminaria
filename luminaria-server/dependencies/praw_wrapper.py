import praw

from common.enums import DEPENDENCY
from database.config.global_config_model import GlobalConfigModel
from dependencies.base_dependency import Dependency


class RedditScanRequest:

    def __init__(self, subreddit_name, limit=25, upvote_threshold=-1):
        self.subreddit_name = subreddit_name
        self.limit = limit
        self.upvote_threshold = upvote_threshold


class PrawWrapper(Dependency):
    DEPENDENCY_ID = DEPENDENCY.PRAW_WRAPPER

    def __init__(self):
        super().__init__()
        self.reddit = praw.Reddit(client_id=GlobalConfigModel.retrieve('CLIENT_ID'),
                                  client_secret=GlobalConfigModel.retrieve('CLIENT_SECRET'),
                                  user_agent='Test Script2')

    def scan_hot(self, sub):
        submissions = []
        for submission in self.reddit.subreddit(sub.subreddit_name).hot(limit=sub.limit):
            if submission.score > sub.upvote_threshold:
                submissions.append(submission)
        return submissions
