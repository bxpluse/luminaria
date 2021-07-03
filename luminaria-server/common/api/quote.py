import yfinance as yf
from common.abstract_classes.candle import Candle
from common.timeless import DATE_FORMAT, TIME_FORMAT, DATETIME_FORMAT
import pandas as pd


class YCandle(Candle):

    def __init__(self, dataframe):
        super().__init__()
        self.dataframe = dataframe
        self.dataframe.columns = map(str.upper, self.dataframe.columns)
        self.datetime_index = pd.to_datetime(self.dataframe.index, format=DATETIME_FORMAT)

    def get_close(self):
        return round(float(self.dataframe.iloc[0]['CLOSE']), 4)

    def get_date(self):
        return self.datetime_index.strftime(DATE_FORMAT)[0]

    def get_time(self):
        return self.datetime_index.strftime(TIME_FORMAT)[0]


def get_close(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1d', interval='30m')
    last_row = hist.tail(1)
    candle = YCandle(last_row)
    return candle


def get_current(symbol):
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='1d', interval='1m')
    last_row = hist.tail(1)
    candle = YCandle(last_row)
    return candle
