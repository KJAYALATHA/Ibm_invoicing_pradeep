import inspect
from datetime import datetime

from dateutil import parser

from log_handler import custom_logger

log = custom_logger()


def get_format_time():
    """
    method to get the formatted time
    :return: formatted time in hhmmss
    """
    try:
        # current date and time
        now = datetime.now()
        # get the formatted time value
        date_time = now.strftime("%d%b%Y_%H%M%S") + str(now.microsecond)
        return date_time
    except Exception as ex:
        log.error("Function {} failed with error : {}".format(inspect.stack()[0][3], ex))


def get_formatted_date(str_date, date_format):
    """
    method to parse the date string to given format
    :param str_date: date as a string
    :param date_format: data time format
    :return: date in a format specified by user
    """
    formatted_date = None
    try:
        formatted_date = parser.parse(str_date).strptime(str_date, "%d/%m/%Y").strftime(date_format)
    except ValueError as ex:
        log.error("Function {} failed with error : {}".format(inspect.stack()[0][3], ex))
    return formatted_date

# print(get_formatted_date("06/04/2022", "%d %b %Y"))
