from datetime import datetime

from peewee import *

from common.util import type_transform
from constants import DB_CONFIG, DB_DYNAMIC, DB_STATIC, DB_STREAM


class ConfigModel(Model):
    class Meta:
        database = DB_CONFIG
        table_name = 'CONFIG_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])

    @staticmethod
    def retrieve_config(model, param, default):
        try:
            res = model.get(model.parameter == param)
            return type_transform(res.value, res.data_type)
        except DoesNotExist:
            if not default:
                raise Exception('DoesNotExist')
            return default
        except OperationalError:
            if not default:
                raise Exception('OperationalError')
            return default


class DynamicModel(Model):

    datetime_created = DateTimeField(default=datetime.now)

    class Meta:
        database = DB_DYNAMIC
        table_name = 'DYNAMIC_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])


class StaticModel(Model):
    class Meta:
        database = DB_STATIC
        table_name = 'STATIC_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])


class StreamModel(Model):
    class Meta:
        database = DB_STREAM
        table_name = 'STREAM_MODEL'

    @classmethod
    def get_table_name(cls):
        return cls._meta.table_name

    @classmethod
    def regenerate(cls):
        cls.drop_table([cls])
        cls.create_table([cls])
