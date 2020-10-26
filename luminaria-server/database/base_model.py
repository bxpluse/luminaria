from peewee import *

from vars import DB


class BaseModel(Model):
    class Meta:
        database = DB
        table_name = 'BASE_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls, table):
        cls.drop_table([table])
        cls.create_table([table])
