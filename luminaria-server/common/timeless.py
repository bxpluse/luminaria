from datetime import datetime, timedelta
import random


TIME_FORMAT = '%Y-%m-%d'


def months_diff(from_date, to_date):
    """
    Returns the number of months bewterrn from and to.
    :param from_date: str date
    :param to_date: str date
    :return: int
    """
    d1 = datetime.strptime(to_date, TIME_FORMAT)
    d2 = datetime.strptime(from_date, TIME_FORMAT)
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


def is_weekend(date: str):
    """
    Checks if a date is a weekend.
    :param date: String formatted as TIME_FORMAT
    :return: bool
    """
    d = datetime.strptime(date, TIME_FORMAT)
    week_num = d.weekday()
    if week_num < 5:
        return False
    return True


def next_day(date: str):
    """
    :param date: Current date
    :return: Next day
    """
    tommorrow = datetime.strptime(date, TIME_FORMAT) + timedelta(days=1)
    return tommorrow.strftime(TIME_FORMAT)


def prev_day(date: str):
    """
    :param date: Current date
    :return: Previous day
    """
    tommorrow = datetime.strptime(date, TIME_FORMAT) + timedelta(days=-1)
    return tommorrow.strftime(TIME_FORMAT)