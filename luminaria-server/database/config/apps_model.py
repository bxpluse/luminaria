from peewee import *
from playhouse.shortcuts import model_to_dict

from database.base_model import ConfigModel


class AppsModel(ConfigModel):
    id = CharField(unique=True)
    name = CharField()
    description = CharField(null=True)
    image = CharField(null=True)
    url = CharField()
    is_online = BooleanField()
    order = IntegerField()

    class Meta:
        table_name = 'APPS'

    @staticmethod
    def get_all_online_apps():
        res = {}
        for app in AppsModel.select():
            if app.is_online:
                res[app.id] = model_to_dict(app)
        return res
