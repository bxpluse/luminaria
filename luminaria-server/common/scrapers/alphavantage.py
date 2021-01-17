import json
from enum import Enum

import requests

from common.util import str_to_float, flaot_to_float
from config import ALPHA_VANTAGE_KEY
from database.timeseries.daily_adjusted_model import TimeSeriesDailyAdjustedModel
from vars import DB1


class ParamOutputSize(Enum):
    COMPACT = 'compact'
    FULL = 'full'


class DataType(Enum):
    JSON = 'json'
    CSV = 'csv'


def time_series_adjusted_download(symbol, update=False):
    outputsize = ParamOutputSize.FULL.value
    if update:
        outputsize = ParamOutputSize.COMPACT.value
    datatype = DataType.JSON.value
    symbol = symbol.upper()
    url = 'https://www.alphavantage.co/query?' \
          'function=TIME_SERIES_DAILY_ADJUSTED&' \
          'symbol={0}&outputsize={1}&datatype={2}&apikey={3}' \
        .format(symbol, outputsize, datatype, ALPHA_VANTAGE_KEY)

    r = requests.get(url)

    json_string = r.text
    obj = json.loads(json_string)['Time Series (Daily)']

    with DB1.transaction() as txn:
        for key, value in obj.items():
            m_open = str_to_float(value['1. open'])
            high = str_to_float(value['2. high'])
            low = str_to_float(value['3. low'])
            close = str_to_float(value['4. close'])
            adjusted_close = str_to_float(value['5. adjusted close'])

            percent = adjusted_close / close

            TimeSeriesDailyAdjustedModel.insert(
                symbol=symbol,
                date=key,

                open=m_open,
                high=high,
                low=low,
                close=close,

                adjusted_open=flaot_to_float(m_open * percent),
                adjusted_high=flaot_to_float(high * percent),
                adjusted_low=flaot_to_float(low * percent),
                adjusted_close=adjusted_close,

                volume=int(value['6. volume']),
                dividend_amount=str_to_float(value['7. dividend amount']),
                split_coefficient=str_to_float(value['8. split coefficient'])
            ).on_conflict_ignore().execute()
        txn.commit()


if __name__ == "__main__":
    pass
