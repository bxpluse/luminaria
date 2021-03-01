from peewee import *

from vars import DB1, DB2, DB_STREAM


class BaseModel(Model):
    class Meta:
        database = DB1
        table_name = 'BASE_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls, table):
        cls.drop_table([table])
        cls.create_table([table])


class StaticModel(Model):
    class Meta:
        database = DB2
        table_name = 'STATIC_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls, table):
        cls.drop_table([table])
        cls.create_table([table])


class StreanModel(Model):
    class Meta:
        database = DB_STREAM
        table_name = 'STREAM_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls, table):
        cls.drop_table([table])
        cls.create_table([table])