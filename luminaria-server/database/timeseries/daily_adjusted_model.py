from peewee import *
from playhouse.shortcuts import model_to_dict

from database.base_model import StaticModel


class TimeSeriesDailyAdjustedModel(StaticModel):

    symbol = CharField()

    date = DateField()

    open = FloatField()
    high = FloatField()
    low = FloatField()
    close = FloatField()

    adjusted_open = FloatField()
    adjusted_high = FloatField()
    adjusted_low = FloatField()
    adjusted_close = FloatField()

    volume = IntegerField()
    dividend_amount = FloatField()
    split_coefficient = FloatField()

    class Meta:
        table_name = 'TIME_SERIES_DAILY_ADJUSTED'
        indexes = (
            (('symbol', 'date'), True),
        )


if __name__ == "__main__":
    t = TimeSeriesDailyAdjustedModel
    t.regenerate(TimeSeriesDailyAdjustedModel)
