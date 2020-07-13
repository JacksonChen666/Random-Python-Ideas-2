import datetime as dt


def unix(year: int, month: int, day: int, hour: int, minutes: int):
    return dt.datetime(year, month, day, hour, minutes).timestamp()


def inBetweenTime(end, start, flip=False):
    """Usage:
    start must have year, month, day, hours, minutes, and maybe seconds
    """
    if flip: end, start = start, end
    start, end = dt.datetime(*start), dt.datetime(*end)

    c = end - start
    print('Difference: ', c)
    return c


if __name__ == '__main__':
    from os import sep, extsep

    print(f"Use \"import {str(__file__).rpartition(sep)[2].rstrip(f'{extsep}py')}\" in your code/console")
