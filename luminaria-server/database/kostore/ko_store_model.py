from peewee import *

from database.base_model import DynamicModel


class KOStoreModel(DynamicModel):
    key = CharField(primary_key=True)
    value = TextField()
    metadata = TextField()
    datetime_updated = DateTimeField()

    class Meta:
        table_name = 'KO_STORE'


if __name__ == "__main__":
    KOStoreModel.regenerate()
