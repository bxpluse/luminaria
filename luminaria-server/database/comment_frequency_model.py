from datetime import date, datetime

from peewee import *

from database.base_model import BaseModel


class CommentFrequencyModel(BaseModel):
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
        for key, value in kwargs.items():
            CommentFrequencyModel.create(
                date=today,
                time=now,
                symbol=key,
                times_mentioned=value,
            )


if __name__ == "__main__":
    model = CommentFrequencyModel()
    model.regenerate(CommentFrequencyModel)
