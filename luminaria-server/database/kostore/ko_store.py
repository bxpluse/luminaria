import json
from datetime import datetime

from peewee import DoesNotExist

from common.transformer import model_to_dict_unstringify
from database.kostore.ko_store_model import KOStoreModel


class KOStore:
    METADATA = '<!METADATA>'

    def __init__(self):
        pass

    @staticmethod
    def put(key, obj):

        if type(key) != str:
            raise Exception('KO Key should be type(str)')
        if type(obj) != dict:
            raise Exception('KO Value should be type(dict)')

        # Pop metadata from main value
        metadata = obj.pop(KOStore.METADATA, {})

        if type(metadata) != dict:
            raise Exception('KO Metadata should be type(dict)')

        key = key.upper()
        now = datetime.now()

        # Convert dict type into string
        obj = json.dumps(obj, default=str)
        metadata = json.dumps(metadata, default=str)

        # Update if key already exists in db, otherwise insert
        # Most transactions are expected to be updates
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
    def get(key):
        key = key.upper()
        try:
            query = KOStoreModel.get(KOStoreModel.key == key)
            d = model_to_dict_unstringify(query, keys=['datetime_created', 'datetime_updated'])
            metadata = {KOStore.METADATA: d['metadata']}
            return {**d['value'], **metadata}
        except DoesNotExist:
            return {}

    @staticmethod
    def get_vals(input_keys):
        keys = [key.upper() for key in input_keys]
        query = KOStoreModel.select().where(KOStoreModel.key << keys)
        res = {}
        for row in query:
            d = model_to_dict_unstringify(row, keys=['datetime_created', 'datetime_updated'])
            metadata = {KOStore.METADATA: d['metadata']}
            k = d['key']
            d = {**d['value'], **metadata}
            res[k] = d
        return res

    @staticmethod
    def get_all_metadata():
        query = KOStoreModel.select()
        metadatas = [model_to_dict_unstringify(row, keys=['datetime_created', 'datetime_updated']) for row in query]
        for md in metadatas:
            del md['value']
        return metadatas

    @staticmethod
    def update_metadata(key, value):
        if type(value) == str:
            try:
                value = json.loads(value)
            except json.decoder.JSONDecodeError:
                raise 'Error: KOStore update_metadata failed due to invalid json'
        if type(value) == dict:
            value = json.dumps(value)
        query = (KOStoreModel
                 .update({KOStoreModel.metadata: value})
                 .where(KOStoreModel.key == key))
        query.execute()
