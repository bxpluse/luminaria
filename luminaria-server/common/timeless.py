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


def is_weekend(date):
    """
    Checks if a date is a weekend.
    :param date: A date in TIME_FORMAT
    :return: bool
    """
    if type(date) == str:
        d = datetime.strptime(date, TIME_FORMAT)
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
    tomorrow = datetime.strptime(date, TIME_FORMAT) + timedelta(days=1)
    return tomorrow.strftime(TIME_FORMAT)


def prev_day(date):
    """
    :param date: Current date
    :return: Previous day. Same data type as passed in.
    """
    if type(date) == str:
        tomorrow = datetime.strptime(date, TIME_FORMAT) + timedelta(days=-1)
        return tomorrow.strftime(TIME_FORMAT)
    tomorrow = date + timedelta(days=-1)
    return tomorrow
