from datetime import date, datetime
from enum import Enum

from peewee import *
from playhouse.shortcuts import model_to_dict

from database.base_model import BaseModel


class FOUNDSTATUS(Enum):
    NOT_FOUND = 0
    FOUND = 1
    DISMISSED = 2


class IPOStringModel(BaseModel):
    string_unique = CharField(unique=True)
    string = CharField()
    found = IntegerField()
    found_date = DateField(null=True)
    found_time = TimeField(null=True)

    class Meta:
        table_name = 'IPO_STRINGS'

    @staticmethod
    def get_all_not_found_strings():
        query = IPOStringModel.select().where(IPOStringModel.found == FOUNDSTATUS.NOT_FOUND.value)
        return [item.string_unique for item in query]

    @staticmethod
    def get_all_not_dismissed_strings():
        query = IPOStringModel.select().where(IPOStringModel.found != FOUNDSTATUS.DISMISSED.value)
        return [model_to_dict(item, exclude=[IPOStringModel.found_time]) for item in query]

    @staticmethod
    def insert_string_if_not_exists(string):
        pk = string.upper()
        query = IPOStringModel.select().where(IPOStringModel.string_unique == pk)
        if not query.exists():
            IPOStringModel.create(string_unique=pk, string=string, found=FOUNDSTATUS.NOT_FOUND.value, found_date=None)

    @staticmethod
    def update_string_as_found(string):
        pk = string.upper()
        today = date.today()
        now = datetime.now()
        query = IPOStringModel.update(found=1, found_date=today, found_time=now)\
            .where(IPOStringModel.string_unique == pk)
        query.execute()

    @staticmethod
    def update_string_as_dismissed(string):
        pk = string.upper()
        query = IPOStringModel.update(found=2)\
            .where(IPOStringModel.string_unique == pk)
        query.execute()

    @staticmethod
    def remove_string_if_not_found(string):
        IPOStringModel.delete().where(
            (IPOStringModel.string_unique == string.upper()) &
            (IPOStringModel.found == FOUNDSTATUS.NOT_FOUND.value
             )).execute()
