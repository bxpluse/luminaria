import re
import time

import feedparser
from peewee import IntegrityError

from apps.baseapp import App
from common.abstract_classes.rule import Rule
from common.cache import Cache
from common.enums import APP, APPTYPE
from common.timeless import DATETIME_FORMAT
from common.util import extract_domain
from constants import CONFIG_MAP
from constants import DB_DYNAMIC
from database.dynamic.rss_entry import RSSEntryModel

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
                RSSEntryModel.create(title=entry.title,
                                     author=entry.get('author', None),
                                     published_datetime=time.strftime(DATETIME_FORMAT, entry.published_parsed),
                                     link=entry.link,
                                     summary=clean_html(entry.summary),
                                     tags=str(resolve_tags(entry.get('tags', []))),
                                     media_thumbnail=resolve_media_urls(entry.get('media_thumbnail', {}))
                                     )
            except IntegrityError:
                pass
    return extract_domain(url) + ' scanned'


class Feeds(App):
    APP_ID = APP.FEEDS

    def __init__(self):
        cache = Cache(30)
        super().__init__(app_type=APPTYPE.STREAMING, cache=cache)

        urls = CONFIG_MAP['FEED_SITES']

        rule = Rule('Feed sites')
        rule.description = 'Store a set of feeds'
        rule.app_id = self.APP_ID
        for url in urls:
            rule.create_subrule(
                name=extract_domain(url) + '_feed',
                func=get_feed,
                args=url,
                triggers={
                    'day_of_week': 'sat',
                }
            )
        self.overseer.add_rule(rule)

    def execute(self, command, **kwargs):
        if command == 'entries':
            return {'entries': RSSEntryModel.get_not_dismissed_entries()}
        elif command == 'dismiss':
            RSSEntryModel.dismiss(kwargs['id'])
            return self.execute('entries')
        elif command == 'force-fetch-feed':
            urls = CONFIG_MAP['FEED_SITES']
            for url in urls:
                get_feed(url)
