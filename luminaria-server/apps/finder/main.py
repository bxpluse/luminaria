import tweepy

from apps.baseapp import App
from common.abstract_classes.rule import Rule
from common.cache import Cache
from common.enums import APP, APPTYPE
from database.kostore.ko_store import KOStore


class Finder(App):
    APP_ID = APP.FINDER
    KO_KEY_VTB_SCH = 'VTB_SCH'
    DEFAULT_HOUR = 1

    def __init__(self):
        cache = Cache(30)
        super().__init__(app_type=APPTYPE.STREAMING, cache=cache)
        auth = tweepy.AppAuthHandler(self.configuration['TWITTER_APP_KEY'], self.configuration['TWITTER_APP_SECRET'])
        self.api = tweepy.API(auth)
        self.users = self.configuration['TWITTER_USERS_TO_FETCH_SCHEDULE']

        rule = Rule('Schedule Finder', alarmable=False)
        rule.description = 'Try to find a set of schedules'
        rule.app_id = self.APP_ID
        hour = Finder.DEFAULT_HOUR
        for user in self.users:
            rule.create_subrule(
                name=user + ':sch',
                func=self.get_schedule,
                args=user,
                triggers={
                    'day_of_week': 'mon,tue,wed,thu,fri,sat,sun',
                    'hour': str(hour)
                }
            )
            hour += 1
            if hour > 22:
                hour = Finder.DEFAULT_HOUR
        self.overseer.add_rule(rule)
        self.start()

    def get_schedule(self, user):

        key = Finder.KO_KEY_VTB_SCH + ':' + user
        obj = KOStore.get(key)
        obj['name'] = user
        if 'schedules' not in obj:
            obj['schedules'] = {}

        tweets = self.api.user_timeline(screen_name=user,
                                        count=200,
                                        tweet_mode='extended',
                                        include_rts=False,
                                        exclude_replies=True,
                                        )
        for tweet in tweets:
            if 'schedule' in tweet.full_text.lower():
                if 'media' in tweet.entities:
                    media_urls = []
                    for image in tweet.entities['media']:
                        media_urls.append(image['media_url'])
                    obj['schedules'][tweet.id] = {'tweet_created_at': tweet.created_at, 'media_urls': media_urls}

        KOStore.put(key, obj)

    def execute(self, command, **kwargs):
        if command == 'fetch-schedules':
            list_of_schedules = []
            for user in self.users:
                res = KOStore.get(Finder.KO_KEY_VTB_SCH + ':' + user)
                list_of_schedules.append(res)
            return {'schedules': list_of_schedules}
