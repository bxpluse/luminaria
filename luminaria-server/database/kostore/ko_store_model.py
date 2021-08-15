from datetime import datetime

from peewee import *

from database.base_model import StreamModel


class KOStoreModel(StreamModel):
    key = CharField(primary_key=True)
    value = TextField()
    metadata = TextField()
    datetime_created = DateTimeField(default=datetime.now)
    datetime_updated = DateTimeField()

    class Meta:
        table_name = 'KO_STORE'


if __name__ == "__main__":
    KOStoreModel.regenerate()
