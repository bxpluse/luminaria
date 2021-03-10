import json
from datetime import date

from apps.baseapp import App
from common.enums import APP
from common.timeless import prev_day, is_weekend, day_of_week
from database.comment_frequency_model import CommentFrequencyModel


class TopTen(App):

    APP_ID = APP.TOP_TEN.value

    def __init__(self):
        super().__init__()

    def get_hot(self, num_prev_days, limit):
        res = {}
        day = date.today()
        for _ in range(num_prev_days):
            res[str(day)] = {}
            day_dict = res[str(day)]

            query_total_mention = CommentFrequencyModel.get_total_mentions_on_day(day)
            query_hot = CommentFrequencyModel.get_top_on_day(day, limit)

            day_dict['symbols'] = []
            day_dict['mentions'] = []
            day_dict['is_weekend'] = is_weekend(day)
            day_dict['day_of_week'] = day_of_week(day)
            day_dict['total_mentions'] = query_total_mention.total

            for item in query_hot:
                day_dict['symbols'].append(item.symbol)
                day_dict['mentions'].append(item.total)
            day = prev_day(day)
        return res

    def execute(self, command, **kwargs):
        if command == 'absolute_top':
            num_prev_days = kwargs.get('num_prev_days', 7)
            limit = kwargs.get('limit', 10)
            return {'absolute_top': self.get_hot(num_prev_days, limit)}


if __name__ == "__main__":
    tt = TopTen()
    r = tt.execute('absolute_top')
    print(json.dumps(r, indent=2, sort_keys=True))
