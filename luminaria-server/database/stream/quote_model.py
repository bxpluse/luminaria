from datetime import datetime

from peewee import CharField, FloatField, DateTimeField, DateField, TimeField, fn
from database.base_model import StreamModel


class QuoteModel(StreamModel):
    symbol = CharField()
    field = CharField()
    value = FloatField()
    date = DateField()
    time = TimeField()
    datetime_created = DateTimeField()

    class Meta:
        table_name = 'QUOTE'

    @staticmethod
    def insert_new(symbol, field, value, date, time):
        QuoteModel.create(symbol=symbol.upper(),
                          field=field.upper(),
                          value=float(value),
                          date=date,
                          time=time,
                          datetime_created=datetime.now()
                          )

    @staticmethod
    def fetch_by_symbol_field_date(symbol, field, date):
        query = QuoteModel\
            .select()\
            .where((QuoteModel.symbol == symbol) & (QuoteModel.field == field) & (fn.DATE(QuoteModel.date) == date))
        return [item for item in query]


if __name__ == "__main__":
    QuoteModel.regenerate()
