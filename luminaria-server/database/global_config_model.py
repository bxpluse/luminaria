from peewee import *
from database.base_model import BaseModel


class GlobalConfigModel(BaseModel):
    parameter = CharField(unique=True)
    value = CharField()

    class Meta:
        table_name = 'GLOBAL_CONFIG'

    @staticmethod
    def retrieve(param):
        res = GlobalConfigModel.get(GlobalConfigModel.parameter == param)
        return res.value
