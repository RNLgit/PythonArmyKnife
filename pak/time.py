"""
Time related on stop functions
"""
import time
from datetime import datetime


def datetimestamp(no_microseconds=False):
    """
    returns a timestamp of current local date time. Default will give a precision upto microseconds.
    Format as Date/Month/Year-Hour:Minute:Second.Microsecond
    """
    if no_microseconds:
        return datetime.now().strftime('%m/%d/%Y-%H:%M:%S')
    else:
        return datetime.now().strftime('%m/%d/%Y-%H:%M:%S.%f')


def timestamp():
    """
    returns a pure time stamp precision up to microseconds
    """
    return datetime.now().strftime('%H:%M:%S.%f')


def stopwatch(func):
    """
    A decorator (use before func @stopwatch) takes how long that takes a function to run.
    :param func: func obj without init
    """
    def inner(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        try:
            f_name = func.__name__
        except:
            f_name = ''
        print(f'Lap time of function {f_name}: {end - begin}s')
        return result

    return inner
