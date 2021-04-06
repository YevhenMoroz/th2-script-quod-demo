from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


def tom():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y%m%d')


def broken_1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y%m%d')


def broken_2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=4)).date().strftime('%Y%m%d')


def today():
    return (tm(datetime.utcnow().isoformat()) + bd(n=0)).date().strftime('%Y%m%d')


def spo():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d')


def sn():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y%m%d')


def wk1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d')


def wk2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=12)).date().strftime('%Y%m%d')


def wk3():
    return (tm(datetime.utcnow().isoformat()) + bd(n=17)).date().strftime('%Y%m%d')


def m1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=25)).date().strftime('%Y%m%d')


def m2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=47)).date().strftime('%Y%m%d')


def m3():
    return (tm(datetime.utcnow().isoformat()) + bd(n=68)).date().strftime('%Y%m%d')


def m4():
    return (tm(datetime.utcnow().isoformat()) + bd(n=90)).date().strftime('%Y%m%d')


def y1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=263)).date().strftime('%Y%m%d')


def y2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=524)).date().strftime('%Y%m%d')


def tom_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y-%m-%d %H:%M:%S')


def broken_1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y-%m-%d %H:%M:%S')


def broken_2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=4)).date().strftime('%Y-%m-%d %H:%M:%S')


def next_monday_front_end():
    monday = 6 - int(datetime.now().strftime('%w'))
    return (tm(datetime.utcnow().isoformat()) + bd(n=monday)).date().strftime('%Y-%m-%d %H:%M:%S')


def today_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=0)).date().strftime('%Y-%m-%d %H:%M:%S')


def spo_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d %H:%M:%S')


def sn_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y-%m-%d %H:%M:%S')


def wk1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y-%m-%d %H:%M:%S')


def wk2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=12)).date().strftime('%Y-%m-%d %H:%M:%S')


def wk3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=17)).date().strftime('%Y-%m-%d %H:%M:%S')


def m1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=25)).date().strftime('%Y-%m-%d %H:%M:%S')


def m2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=47)).date().strftime('%Y-%m-%d %H:%M:%S')


def m3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=68)).date().strftime('%Y-%m-%d %H:%M:%S')


def m4_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=90)).date().strftime('%Y-%m-%d %H:%M:%S')


def next_working_day_after_25dec_front_end():
    return (tm(datetime(2021, 12, 25).isoformat()) + bd(n=0)).date().strftime('%Y-%m-%d %H:%M:%S')


def y1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=263)).date().strftime('%Y-%m-%d %H:%M:%S')


def y2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=524)).date().strftime('%Y-%m-%d %H:%M:%S')

# TODO need to add another tenors
