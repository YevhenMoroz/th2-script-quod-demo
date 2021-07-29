import math
from datetime import datetime


def round_decimals_up(number: float, decimals: int):
    """
    Returns a value rounded up to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.ceil(number)

    factor = 10 ** decimals
    return math.ceil(number * factor) / factor


def round_decimals_down(number: float, decimals: int):
    """
    Returns a value rounded down to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more")
    elif decimals == 0:
        return math.floor(number)

    factor = 10 ** decimals
    return math.floor(number * factor) / factor


def random_qty(number: int):
    """
    Generate random number with length -> number
    """
    now = datetime.now()
    timestamp = str(datetime.timestamp(now))
    qty = timestamp.replace(".", "")[-number:]
    return qty


def shorting_qty_for_di(qty, currency):
    """
    Returns a short value of qty and adds currency to it
    """
    k = "K"
    m = "M"
    b = "B"
    short_qty = ""
    thousand = range(1, 7)
    million = range(8, 10)
    billion = range(11, 13)
    if len(qty) in thousand:
        short_qty = qty[0:3] + "." + qty[3:5] + k + " " + currency
    if len(qty) in million:
        short_qty = qty[0:3] + "." + qty[3:5] + m + " " + currency
    if len(qty) in billion:
        short_qty = qty[0:3] + "." + qty[3:5] + b + " " + currency
    return short_qty
