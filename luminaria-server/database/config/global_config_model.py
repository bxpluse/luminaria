from peewee import *

from common.util import type_transform
from database.base_model import ConfigModel


class GlobalConfigModel(ConfigModel):
    parameter = CharField(unique=True)
    value = CharField()
    description = CharField(null=True)
    name = CharField(null=True)
    data_type = CharField(null=True)

    class Meta:
        table_name = 'GLOBAL_CONFIG'

    @staticmethod
    def retrieve(param):
        res = GlobalConfigModel.get(GlobalConfigModel.parameter == param)
        return type_transform(res.value, res.data_type)

    @staticmethod
    def retrieve_all():
        # Retrieves all key, value pairs as a dictionary
        query = GlobalConfigModel.select()
        d = {}
        for config in query:
            d[config.parameter] = type_transform(config.value, config.data_type)
        return d
