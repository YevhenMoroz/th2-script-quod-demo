import math
import random
from datetime import datetime
from random import randint


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


# def random_qty(from_number: int, to_number: int, len: int):
#     """
#     Generate random number with length -> len and without 0
#     """
#     multiplier = (str("{:." + str(len) + "f}")).format(1).replace(".", "")
#     multiplier = int(multiplier[:-1])
#     from_number *= multiplier
#     to_number *= multiplier
#     qty = str(randint(from_number, to_number)).replace("0", str(randint(1, 9)))
#     return qty


def random_qty(from_number: int, to_number: int, len: int):
    second_part = ''
    for _ in range(0, len - 1):
        second_part = f'{second_part}{random.randint(1, 9)}'
    return str(random.randint(from_number, to_number - 1)) + str(second_part)


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
