from peewee import *
from playhouse.shortcuts import model_to_dict

from database.base_model import BaseModel


class LinkModel(BaseModel):
    app_id = CharField(unique=True)
    link_to = CharField()

    class Meta:
        table_name = 'LINKS'

    @staticmethod
    def select_link_by_app_id(app_id):
        res = None
        try:
            obj = LinkModel.select().where(LinkModel.app_id == app_id).get()
            res = model_to_dict(obj)['link_to']
        except Exception:
            pass
        return res
