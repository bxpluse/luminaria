import json
from datetime import datetime

from peewee import DoesNotExist

from common.transformer import model_to_dict_unstringify
from database.kostore.ko_store_model import KOStoreModel


class KOStore:

    def __init__(self):
        pass

    @staticmethod
    def put(key, obj, metadata=None):
        if metadata is None:
            metadata = {}
        if type(key) != str:
            raise Exception('KO Key should be type(str)')
        if type(obj) != dict:
            raise Exception('KO Value should be type(dict)')
        if type(metadata) != dict:
            raise Exception('KO Metadata should be type(dict)')

        key = key.upper()
        obj = json.dumps(obj, default=str)
        metadata = json.dumps(metadata, default=str)
        now = datetime.now()

        num_updated = KOStoreModel.update(key=key,
                                          value=obj,
                                          metadata=metadata,
                                          datetime_updated=now) \
            .where(KOStoreModel.key == key) \
            .execute()

        if num_updated == 0:
            KOStoreModel.insert(key=key,
                                value=obj,
                                metadata=metadata,
                                datetime_updated=now) \
                .execute()

    @staticmethod
    def get(key, column='value'):
        key = key.upper()
        try:
            query = KOStoreModel.get(KOStoreModel.key == key)
            return model_to_dict_unstringify(query, keys=['datetime_created', 'datetime_updated'])[column]
        except DoesNotExist:
            return {}
