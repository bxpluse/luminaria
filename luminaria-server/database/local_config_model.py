from peewee import *

from database.base_model import BaseModel


class LocalConfigModel(BaseModel):
    parameter = CharField(unique=True)
    value = CharField()
    description = CharField(null=True)
    name = CharField(null=True)

    class Meta:
        table_name = 'LOCAL_CONFIG'

    @staticmethod
    def retrieve(param):
        res = LocalConfigModel.get(LocalConfigModel.parameter == param)
        return res.value
