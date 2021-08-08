from peewee import *

from database.base_model import DynamicModel


class KOStore(DynamicModel):
    key = CharField()
    value = TextField()
    datetime_updated = DateTimeField()

    class Meta:
        table_name = 'KO_STORE'

    @staticmethod
    def put(key, obj):
        pass

    @staticmethod
    def get(key):
        pass


if __name__ == "__main__":
    KOStore.regenerate()
