import json
import re
import time
from datetime import datetime

import feedparser
from peewee import IntegrityError

from apps.baseapp import App
from common.abstract_classes.rule import Rule
from common.cache import Cache
from common.enums import APP, APPTYPE, Variant
from common.messenger import Toast
from common.timeless import DATETIME_FORMAT
from common.util import extract_domain
from constants import DB_DYNAMIC, EMPTY_JSON_DICT
from database.dynamic.feed_entry_model import FeedEntryModel
from dependencies.praw_wrapper import RedditScanRequest

CLEAN_REGEX = re.compile('<.*?>')


def resolve_tags(tags_list):
    tags = set()
    for tags_dict in tags_list:
        for value in tags_dict.values():
            if value is not None:
                tags.add(value)
    return list(tags)


def resolve_media_urls(media_thumbnails):
    for thumbnail in media_thumbnails:
        if 'url' in thumbnail:
            return thumbnail['url']
    return None


def clean_html(raw_html):
    clean_text = re.sub(CLEAN_REGEX, '', raw_html)
    return clean_text


def get_feed(url):
    try:
        rss_dict = feedparser.parse(url)
    except Exception as e:
        return 'Error: ' + str(e)
    with DB_DYNAMIC.atomic():
        for entry in rss_dict.entries:
            try:
                FeedEntryModel.create(title=entry.title,
                                      author=entry.get('author', None),
                                      published_datetime=time.strftime(DATETIME_FORMAT, entry.published_parsed),
                                      link=entry.link,
                                      summary=clean_html(entry.summary),
                                      tags=str(resolve_tags(entry.get('tags', []))),
                                      media_thumbnail=resolve_media_urls(entry.get('media_thumbnail', {})),
                                      type='RSS',
                                      metadata=EMPTY_JSON_DICT,
                                      )
            except IntegrityError:
                pass
    return extract_domain(url) + ' scanned'


class Feeds(App):
    APP_ID = APP.FEEDS

    def __init__(self):
        cache = Cache(30, exclusion=('dismiss', 'force-fetch-feed', 'vote'))
        super().__init__(app_type=APPTYPE.STREAMING, cache=cache)
        self.create_rss_feeds()
        self.create_subreddit_feeds()
        self.start()

    def create_rss_feeds(self):
        urls = self.configuration['RSS_FEED_SITES']
        rule = Rule('RSS feeds', alarmable=False)
        rule.description = 'Store a set of RSS feeds'
        rule.app_id = self.APP_ID
        for url in urls:
            rule.create_subrule(
                subrule_name=extract_domain(url) + '_feed',
                func=get_feed,
                args=url,
                triggers={
                    'day_of_week': 'sat',
                }
            )
        self.overseer.add_rule(rule)

    def create_subreddit_feeds(self):
        subs = self.configuration['SUBREDDIT_FEED_SITES']
        rule = Rule('Subreddit feeds', alarmable=False)
        rule.description = 'Store a set of Subreddit feeds'
        rule.app_id = self.APP_ID
        for sub_name in subs:
            rule.create_subrule(
                subrule_name=sub_name + '_feed',
                func=self.get_submissions,
                args=sub_name,
                triggers={
                    'hour': '5',
                }
            )
        self.overseer.add_rule(rule)

    def get_submissions(self, subreddit):
        rsr = RedditScanRequest(subreddit_name=subreddit)
        submissions = self.praw_wrapper.scan_hot(rsr)
        with DB_DYNAMIC.atomic():
            for submission in submissions:
                # Insert new row or update metadata of existing row
                metadata = {'num_comments': submission.num_comments,
                            'score': submission.score,
                            'upvote_ratio': submission.upvote_ratio,
                            'url': submission.url
                            }
                if len(submission.selftext) > 500:
                    summary = submission.selftext[0:497] + ' ...'
                else:
                    summary = submission.selftext
                FeedEntryModel.insert(title=submission.title,
                                      author=submission.author,
                                      published_datetime=datetime.utcfromtimestamp(submission.created_utc)
                                      .strftime(DATETIME_FORMAT),
                                      link=self.configuration['REDDIT_BASE_URL'] + submission.permalink,
                                      summary=summary,
                                      tags=str([]),
                                      media_thumbnail=resolve_media_urls({}),
                                      type='SUBREDDIT',
                                      metadata=json.dumps(metadata),
                                      ) \
                    .on_conflict(conflict_target=[FeedEntryModel.link], preserve=[FeedEntryModel.metadata]) \
                    .execute()
        return subreddit + ' scanned'

    def execute(self, command, **kwargs):
        if command == 'entries':
            return {'entries': FeedEntryModel.get_not_dismissed_entries()}
        elif command == 'dismiss':
            self.cache.invalidate()
            FeedEntryModel.dismiss(kwargs['id'])
            return self.execute('entries')
        elif command == 'vote':
            self.cache.invalidate()
            FeedEntryModel.vote(kwargs['id'], kwargs['points'])
            return {**self.execute('entries'), **{Toast.IDENTIFIER: Toast('+1', variant=Variant.INFO, duration=1)}}
        elif command == 'force-fetch-feed':
            self.cache.invalidate()
            urls = self.configuration['RSS_FEED_SITES']
            for url in urls:
                get_feed(url)
            subreddits = self.configuration['SUBREDDIT_FEED_SITES']
            for subreddit in subreddits:
                self.get_submissions(subreddit)
