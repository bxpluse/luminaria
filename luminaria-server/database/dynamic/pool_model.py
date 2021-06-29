from datetime import datetime

from peewee import CharField, FloatField, BooleanField, TimeField, DateField
from playhouse.shortcuts import model_to_dict

from common.transformer import model_to_dict_wrapper
from database.base_model import DynamicModel

DATETIME_KEYS = ['datetime_created', 'date', 'time', 'expiry_date']


class PoolModel(DynamicModel):
    pool_name = CharField(unique=True)
    description = CharField()
    is_active = BooleanField()

    class Meta:
        table_name = 'POOL'

    @staticmethod
    def get_all_pools():
        query = PoolModel.select()
        pools = [model_to_dict(pool) for pool in query]
        return pools

    @staticmethod
    def get_pool_entries_by_name(pool_name):
        query = PoolTransactionModel.select().where(PoolTransactionModel.pool_name == pool_name)
        query2 = PoolTradeModel.select().where(PoolTradeModel.pool_name == pool_name)
        entries = [model_to_dict_wrapper(entry, keys=DATETIME_KEYS) for entry in query]
        entries += [model_to_dict_wrapper(entry, keys=DATETIME_KEYS) for entry in query2]
        sorted_entries = sorted(entries, key=lambda k: (k['date'], k['time']))
        return sorted_entries


class PoolTradeModel(DynamicModel):
    pool_name = CharField()
    instrument = CharField()
    action = CharField()
    amount = FloatField()
    symbol = CharField()
    price = FloatField()
    date = DateField()
    time = TimeField()
    is_open = BooleanField()
    spot = FloatField(null=True)
    strike = FloatField(null=True)
    expiry_date = DateField(null=True)
    note = CharField()

    class Meta:
        table_name = 'POOL_TRADE'

    @staticmethod
    def insert_entry_by_name(pool_name, instrument, action, amount, symbol, price, date,
                             time, spot, strike, expiry_date, note):
        PoolTradeModel.create(pool_name=pool_name,
                              instrument=instrument,
                              action=action,
                              amount=amount,
                              symbol=symbol,
                              price=price,
                              date=date,
                              time=time,
                              is_open=True,
                              spot=spot,
                              strike=strike,
                              expiry_date=expiry_date,
                              note=note,
                              datetime_created=datetime.now())


class PoolTransactionModel(DynamicModel):
    pool_name = CharField()
    action = CharField()
    amount = FloatField()
    date = DateField()
    time = TimeField()

    class Meta:
        table_name = 'POOL_TRANSACTION'


if __name__ == "__main__":
    PoolModel.regenerate()
    PoolTradeModel.regenerate()
    PoolTransactionModel.regenerate()
