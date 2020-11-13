from datetime import date
from collections import defaultdict
from apps.baseapp import App
from database.comment_frequency_model import CommentFrequencyModel
from playhouse.shortcuts import model_to_dict
from vars import DB

class WordCloud(App):
    """
        Updates CSV file of exchanges.
    """

    APP_ID = 'wordcloud'

    def __init__(self):
        super().__init__()

    def run(self):
        super().start()

        #  select Id, sum(Amount) as TotalSum from SumOfEveryDistinct
        #    -> group by Id;

        #res = defaultdict(lambda: 0, {})
        #for item in CommentFrequencyModel.select().where(CommentFrequencyModel.date == date.today()):
        #    res[item.symbol] += item.times_mentioned
        #for key, value in res.items():
        #    print(key, value)

        cursor = DB.execute_sql('''select *, sum(times_mentioned) as total
                                from COMMENT_FREQUENCY where date=?
                                group by symbol
                                order by total desc'''
                                , (date.today(),))

        for row in cursor.fetchall():
            print(row)


        super().stop()


wc = WordCloud()
wc.run()
