from datetime import datetime, date

from apps.baseapp import App
from common.enums import APP
from database.dynamic.pool_model import PoolModel, PoolTransactionModel, PoolTradeModel


class PoolAction:
    BUY = 'BUY'
    SELL = 'SELL'
    DEPOSIT = 'DEPOSIT'
    WITHDRAW = 'WITHDRAW'


class Pool(App):
    APP_ID = APP.POOL

    def __init__(self):
        super().__init__()

    @staticmethod
    def create_pool(pool_name, description, initial_fund):
        dt = datetime.now()
        PoolModel.create(
            pool_name=pool_name,
            description=description,
            is_active=True,
            datetime_created=dt

        )
        PoolTransactionModel.create(
            pool_name=pool_name,
            action=PoolAction.DEPOSIT,
            amount=initial_fund,
            date=date.today(),
            time=dt.strftime("%H:%M:%S"),
            datetime_created=dt
        )

    @staticmethod
    def fetch_all_pools():
        return PoolModel.get_all_pools()

    @staticmethod
    def fetch_pool_entries_by_name(pool_name):
        return PoolModel.get_pool_entries_by_name(pool_name)

    def execute(self, command, **kwargs):
        if command == 'createPool':
            name = kwargs['poolName']
            description = kwargs['description']
            initial_fund = kwargs['initialFund']
            self.create_pool(name, description, initial_fund)
            return {}
        elif command == 'fetchAllPoolNames':
            return {'pools': self.fetch_all_pools()}
        elif command == 'fetchPoolEntriesByName':
            name = kwargs['poolName']
            return {'entries': self.fetch_pool_entries_by_name(name)}
        elif command == 'saveEntryByName':
            instrument = kwargs['instrument'].upper()
            pool_name = kwargs['poolName']
            entry_type = kwargs['entryType'].upper()
            action = kwargs['action']
            amount = float(kwargs['amount'])
            symbol = kwargs['symbol'].upper()
            price = float(kwargs['price'])
            date_ = kwargs['date']
            time_ = kwargs['time']
            spot = None
            strike = None
            expiry_date = None
            note = kwargs['note']
            if entry_type == 'option':
                spot = float(kwargs['spot'])
                strike = float(kwargs.get('strike', 0))
                expiry_date = kwargs['expiryDate']
            PoolTradeModel \
                .insert_entry_by_name(pool_name, instrument, action, amount,
                                      symbol, price, date_, time_, spot, strike, expiry_date, note)
            return {}
