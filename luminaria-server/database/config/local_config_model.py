from peewee import *

from common.util import type_transform
from database.base_model import ConfigModel


class LocalConfigModel(ConfigModel):
    parameter = CharField(unique=True)
    value = CharField()
    description = CharField(null=True)
    name = CharField(null=True)
    data_type = CharField(null=True)

    class Meta:
        table_name = 'LOCAL_CONFIG'

    @staticmethod
    def retrieve(param):
        res = LocalConfigModel.get(LocalConfigModel.parameter == param)
        return type_transform(res.value, res.data_type)

    @staticmethod
    def retrieve_default(param, default):
        try:
            res = LocalConfigModel.get(LocalConfigModel.parameter == param)
            return type_transform(res.value, res.data_type)
        except DoesNotExist:
            return default
        except OperationalError:
            return default

    @staticmethod
    def retrieve_all():
        # Retrieves all key, value pairs as a dictionary
        query = LocalConfigModel.select()
        d = {}
        for config in query:
            d[config.parameter] = type_transform(config.value, config.data_type)
        return d
