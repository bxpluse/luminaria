import numpy as np

from common.enums import TimeFrame
from common.exceptions import DateMismatchException
from common.timeless import months_diff, random_year, random_month
from database.timeseries.daily_adjusted_model import TimeSeriesDailyAdjustedModel


class BetaResult:

    def __init__(self):
        self.beta = None
        self.cov_matrix = None
        self.var1 = None
        self.var2 = None


def get_beta(instrument1, instrument2, timeframe, from_date='2000-01-01', to_date='2021-01-01'):
    query1 = (TimeSeriesDailyAdjustedModel.select()
              .where((TimeSeriesDailyAdjustedModel.symbol == instrument1)
                     & (TimeSeriesDailyAdjustedModel.date > from_date)
                     & (TimeSeriesDailyAdjustedModel.date < to_date)
                     )
              .order_by(TimeSeriesDailyAdjustedModel.date.asc()))

    query2 = (TimeSeriesDailyAdjustedModel.select()
              .where((TimeSeriesDailyAdjustedModel.symbol == instrument2)
                     & (TimeSeriesDailyAdjustedModel.date > from_date)
                     & (TimeSeriesDailyAdjustedModel.date < to_date)
                     )
              .order_by(TimeSeriesDailyAdjustedModel.date.asc()))

    if len(query1) != len(query2):
        raise DateMismatchException('Dates between instruments mismatch.')
    if from_date == to_date:
        raise DateMismatchException('From date and to date is the same.')
    if months_diff(from_date, to_date) < 4:
        raise DateMismatchException('From date and to date too close together.')

    prices1, prices2 = sort_time(query1, query2, timeframe, 'adjusted_close')

    diff1 = np.diff(prices1) / prices1[:-1] * 100
    diff2 = np.diff(prices2) / prices2[:-1] * 100

    cov_matrix = np.cov(diff1, diff2)
    cov = cov_matrix[0][1]
    var1 = np.var(diff1)
    var2 = np.var(diff2)

    b1 = cov / var2

    res = BetaResult()
    res.cov_matrix = cov_matrix
    res.var1 = var1
    res.var2 = var2
    res.beta = round(b1, 4)

    return res


def sort_time(query1, query2, time_frame, column):
    prices1 = []
    prices2 = []

    i = None
    if time_frame == TimeFrame.MONTH_START or time_frame == TimeFrame.WEEK_START:
        i = 0
    elif time_frame == TimeFrame.MONTH_END or time_frame == TimeFrame.WEEK_END:
        i = 1
    prev_date = query1[0].date.month
    for idx in range(len(query1)):

        if time_frame == TimeFrame.MONTH_START or time_frame == TimeFrame.MONTH_END:
            date = query1[idx].date.month
        else:
            date = query1[idx].date.strftime("%V")

        if date != prev_date:
            prev_date = date
            prices1.append(getattr(query1[idx - i], column))
            prices2.append(getattr(query2[idx - i], column))

    return prices1, prices2


def rand_beta_test():
    timeframes = [TimeFrame.MONTH_START, TimeFrame.MONTH_END, TimeFrame.WEEK_START, TimeFrame.WEEK_END]

    from_date = '{0}-{1}-01'.format(random_year(2004, 2019), random_month())
    to_date = '{0}-{1}-01'.format(random_year(2004, 2019), random_month())

    if from_date > to_date:
        from_date, to_date = to_date, from_date

    print(from_date, to_date, months_diff(from_date, to_date))

    for tf in timeframes:
        b = get_beta('QQQ', 'SPY', tf, from_date=from_date, to_date=to_date).beta
        print(tf.name + ": " + str(b))

# rand_beta_test()
