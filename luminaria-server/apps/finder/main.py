import tweepy

from apps.baseapp import App
from common.abstract_classes.rule import Rule
from common.cache import Cache
from common.enums import APP, APPTYPE
from common.logger import LogLevel
from common.ocr import image_to_text
from common.timeless import Interval
from database.kostore.ko_store import KOStore


class Finder(App):
    APP_ID = APP.FINDER
    KO_KEY_VTB_SCH = 'VTB_SCH'

    def __init__(self):
        cache = Cache(60)
        super().__init__(app_type=APPTYPE.STREAMING, cache=cache)
        auth = tweepy.AppAuthHandler(self.configuration['TWITTER_APP_KEY'], self.configuration['TWITTER_APP_SECRET'])
        self.api = tweepy.API(auth)
        self.users = self.configuration['TWITTER_USERS_TO_FETCH_SCHEDULE']

        rule = Rule('Schedule Finder', alarmable=False)
        rule.description = 'Try to find a set of schedules'
        rule.app_id = self.APP_ID

        interval = Interval(hour=1, minute=0)

        for user in self.users:
            rule.create_subrule(
                subrule_name=user + ':sch',
                func=self.get_schedule,
                args=user,
                triggers={
                    'day_of_week': 'mon,tue,wed,thu,fri,sat,sun',
                    'hour': str(interval.hour),
                    'minute': str(interval.minute)
                }
            )
            interval.increment_15_mins()

        self.overseer.add_rule(rule)
        self.start()

    def get_schedule(self, user):
        key = Finder.KO_KEY_VTB_SCH + ':' + user
        obj = KOStore.get(key)
        obj['name'] = user
        if 'schedules' not in obj:
            obj['schedules'] = {}

        checked_url_key = None
        checked_urls_obj = None
        if self.configuration['FINDER_PIC_IDENTIFIER']:
            checked_url_key = Finder.KO_KEY_VTB_SCH + '>' + 'CHECKED_URLS'
            checked_urls_obj = KOStore.get(checked_url_key)
            if 'checked' not in checked_urls_obj:
                checked_urls_obj['checked'] = {}

        tweets = self.api.user_timeline(screen_name=user,
                                        count=200,
                                        tweet_mode='extended',
                                        include_rts=False,
                                        exclude_replies=True,
                                        )
        max_tweet_id = -1
        for tweet in tweets:
            if 'media' in tweet.entities:
                media_urls = []
                for image in tweet.entities['media']:
                    media_urls.append(image['media_url'])
                if 'schedule' in tweet.full_text.lower():
                    obj['schedules'][tweet.id] = {'tweet_created_at': tweet.created_at, 'media_urls': media_urls}
                    max_tweet_id = max(max_tweet_id, tweet.id)
                else:
                    if self.configuration['FINDER_PIC_IDENTIFIER']:
                        for url in media_urls:
                            if url not in checked_urls_obj['checked']:
                                try:
                                    text = image_to_text(url + ':small')
                                    if ('PST' in text or 'PDT' in text) and 'JST' in text:
                                        obj['schedules'][tweet.id] = {'tweet_created_at': tweet.created_at,
                                                                      'media_urls': media_urls}
                                        max_tweet_id = max(max_tweet_id, tweet.id)
                                    checked_urls_obj['checked'][url] = 1
                                except Exception as e:
                                    self.log('Error: ' + str(e), level=LogLevel.ERROR)

        if max_tweet_id != -1:
            obj['latest'] = {**{'tweet_id': max_tweet_id}, **obj['schedules'][max_tweet_id]}
        if self.configuration['FINDER_PIC_IDENTIFIER']:
            KOStore.put(checked_url_key, checked_urls_obj)
        KOStore.put(key, obj)
        return 'Success'

    def execute(self, command, **kwargs):
        if command == 'fetch-schedules':
            keys = [Finder.KO_KEY_VTB_SCH + ':' + user for user in self.users]
            list_of_schedules = []
            res = KOStore.get_vals(keys)
            for key, value in res.items():
                # Allow only non-empty values through
                if len(value) < 3:
                    continue
                # Remove schedules as it grows to infinity
                if 'schedules' in value:
                    del value['schedules']
                # Convert tweet_id from int to string to prevent floating point error
                value['latest']['tweet_id'] = str(value['latest']['tweet_id'])
                list_of_schedules.append(value)

            # Sort by order if the key exists
            list_of_schedules = sorted(list_of_schedules, key=lambda k: (k[KOStore.METADATA].get('order', 9999)))
            return {'schedules': list_of_schedules}

        elif command == 'force-update-schedules':
            for user in self.users:
                self.get_schedule(user)
