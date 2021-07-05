from datetime import date, datetime

from peewee import *

from database.base_model import StreamModel


class CommentFrequencyModel(StreamModel):
    date = DateField()
    time = TimeField()
    symbol = CharField()
    times_mentioned = IntegerField()

    class Meta:
        table_name = 'COMMENT_FREQUENCY'

    @staticmethod
    def insert_interval(**kwargs):
        today = date.today()
        now = datetime.now()
        with CommentFrequencyModel._meta.database.atomic():
            for key, value in kwargs.items():
                CommentFrequencyModel.create(
                    date=today,
                    time=now,
                    symbol=key,
                    times_mentioned=value,
                )

    @staticmethod
    def get_first_record_by_symbol(symbol):
        res = CommentFrequencyModel.select().where(CommentFrequencyModel.symbol == symbol).get()
        return res

    @staticmethod
    def get_top_on_day(day, limit):
        query = CommentFrequencyModel.select(CommentFrequencyModel.symbol,
                                             fn.sum(CommentFrequencyModel.times_mentioned).alias('total'))\
            .where(CommentFrequencyModel.date == day)\
            .group_by(CommentFrequencyModel.symbol)\
            .order_by(fn.sum(CommentFrequencyModel.times_mentioned).desc())\
            .limit(limit)
        return query

    @staticmethod
    def get_total_mentions_from_day(day):
        query = CommentFrequencyModel\
            .select(CommentFrequencyModel.date, fn.sum(CommentFrequencyModel.times_mentioned).alias('total')) \
            .where(CommentFrequencyModel.date >= day)\
            .group_by(CommentFrequencyModel.date)
        d = {}
        for day in query:
            d[day.date] = day.total
        return d


"""
cursor = DB1.execute_sql('''select symbol, sum(times_mentioned)
                                            from COMMENT_FREQUENCY 
                                            where date = ?
                                            GROUP BY symbol
                                            ORDER BY sum(times_mentioned) desc
                                            LIMIT ?;''',
                              (day, limit))
"""


if __name__ == "__main__":
    import string
    import random
    args = {}

    for i in range(0, 10000):
        rand_symbol = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
        tm = 99
        args[rand_symbol] = tm

    CommentFrequencyModel.insert_interval(**args)
