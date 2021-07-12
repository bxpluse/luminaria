from datetime import datetime, timedelta
import random

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = '%H:%M:%S'
DATETIME_FORMAT = '{0} {1}'.format(DATE_FORMAT, TIME_FORMAT)


def months_diff(from_date, to_date):
    """
    Returns the number of months bewterrn from and to.
    :param from_date: str date
    :param to_date: str date
    :return: int
    """
    d1 = datetime.strptime(to_date, DATE_FORMAT)
    d2 = datetime.strptime(from_date, DATE_FORMAT)
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def random_year(begin, end):
    """
    Returns a random year in between passed in years inclusive.
    :return: str: [begin, end]
    """
    if type(begin) == str:
        begin = int(begin)
    if type(end) == str:
        end = int(end)
    year = random.randint(begin, end)

    if year <= 9:
        return '0' + str(year)

    return str(year)


def random_month():
    """
    Returns a random month as a string. 01, 02, ... , 12
    :return: str
    """
    month = random.randint(1, 12)
    if month <= 9:
        return '0' + str(month)
    return str(month)


def is_weekend(date):
    """
    Checks if a date is a weekend.
    :param date: A date in TIME_FORMAT
    :return: bool
    """
    if type(date) == str:
        d = datetime.strptime(date, DATE_FORMAT)
        week_num = d.weekday()
    else:
        week_num = date.weekday()
    if week_num < 5:
        return False
    return True


def day_of_week(date):
    """
    Get day of the week.
    """
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    return day_dict[date.weekday()]


def next_day(date: str):
    """
    :param date: Current date
    :return: Next day
    """
    tomorrow = datetime.strptime(date, DATE_FORMAT) + timedelta(days=1)
    return tomorrow.strftime(DATE_FORMAT)


def prev_day(date, num_days=1):
    """
    :param date: Current date
    :param num_days: Number of days before the given one
    :return: Previous day. Same data type as passed in.
    """
    if type(date) == str:
        past_day = datetime.strptime(date, DATE_FORMAT) + timedelta(days=-num_days)
        return past_day.strftime(DATE_FORMAT)
    past_day = date + timedelta(days=-num_days)
    return past_day


def prev_weekday(date):
    """
    :param date: Current date
    :return: Previous weekday.
    """
    date = prev_day(date)
    while is_weekend(date):
        date = prev_day(date)
    return date


def today():
    """
    :return: Today's date
    """
    return datetime.today().strftime(DATE_FORMAT)
