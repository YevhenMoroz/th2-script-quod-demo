from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from datetime import datetime, timedelta


def tom():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y%m%d')

def tom_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S')

def broken_1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y%m%d')


def broken_2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=6)).date().strftime('%Y%m%d')


def broken_w1w2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=8)).date().strftime('%Y%m%d')


def broken_w2w3():
    return (tm(datetime.utcnow().isoformat()) + bd(n=14)).date().strftime('%Y%m%d')


def broken_w3m1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=19)).date().strftime('%Y%m%d')


def today():
    return (tm(datetime.utcnow().isoformat()) + bd(n=0)).date().strftime('%Y%m%d')


def today_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=0)).date().strftime('%Y-%m-%dT%H:%M:%S')


def spo():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y%m%d')


def spo_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%dT%H:%M:%S')


def spo_ndf():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y%m%d')


def spo_ndf_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y-%m-%dT%H:%M:%S')


def sn():
    return (tm(datetime.utcnow().isoformat()) + bd(n=3)).date().strftime('%Y%m%d')


def wk1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y%m%d')


def wk1_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=7)).date().strftime('%Y-%m-%dT%H:%M:%S')


def wk1_ndf():
    return (tm(datetime.utcnow().isoformat()) + bd(n=6)).date().strftime('%Y%m%d')


def wk1_ndf_maturity():
    return (tm(datetime.utcnow().isoformat()) + bd(n=5)).date().strftime('%Y%m%d')


def wk2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=12)).date().strftime('%Y%m%d')


def wk2_java_api():
    return (tm(datetime.utcnow().isoformat()) + bd(n=12)).date().strftime('%Y-%m-%dT%H:%M:%S')


def wk2_ndf():
    return (tm(datetime.utcnow().isoformat()) + bd(n=11)).date().strftime('%Y%m%d')


def wk2_ndf_maturity():
    return (tm(datetime.utcnow().isoformat()) + bd(n=10)).date().strftime('%Y%m%d')


def wk3():
    return (tm(datetime.utcnow().isoformat()) + bd(n=17)).date().strftime('%Y%m%d')


def wk3_ndf():
    return (tm(datetime.utcnow().isoformat()) + bd(n=16)).date().strftime('%Y%m%d')


def wk3_ndf_maturity():
    return (tm(datetime.utcnow().isoformat()) + bd(n=16)).date().strftime('%Y%m%d')


def m1():
    return (tm(datetime.utcnow().isoformat()) + bd(n=25)).date().strftime('%Y%m%d')


def m1_ndf():
    return (tm(datetime.utcnow().isoformat()) + bd(n=24)).date().strftime('%Y%m%d')


def m2():
    return (tm(datetime.utcnow().isoformat()) + bd(n=47)).date().strftime('%Y%m%d')


def m3():
    return (tm(datetime.utcnow().isoformat()) + bd(n=70)).date().strftime('%Y%m%d')


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
    return (tm(datetime.utcnow().isoformat()) + bd(n=22)).date().strftime('%Y-%m-%d %H:%M:%S')


def m2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=46)).date().strftime('%Y-%m-%d %H:%M:%S')


def m3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=68)).date().strftime('%Y-%m-%d %H:%M:%S')


def m4_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=91)).date().strftime('%Y-%m-%d %H:%M:%S')


year = int(datetime.now().year)


def next_working_day_after_25dec_front_end():
    return (tm(datetime(year, 12, 25).isoformat()) + bd(n=0)).date().strftime('%Y-%m-%d %H:%M:%S')


def y1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=263)).date().strftime('%Y-%m-%d %H:%M:%S')


def y2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=524)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_spo_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=1)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_sn_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=2)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_wk1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=6)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_wk2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=11)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_wk3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=16)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_m1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=21)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_m2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=44)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_m3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=66)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_m4_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=88)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_y1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=262)).date().strftime('%Y-%m-%d %H:%M:%S')


def ndf_y2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=522)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_wk1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=5)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_wk2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=10)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_wk3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=15)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_m1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=20)).date().strftime('%Y-%m-%d %H:%M:%S')


def custom(days: int = 2):
    return (tm(datetime.utcnow().isoformat()) + bd(n=days)).date().strftime('%Y%m%d')


def fixing_ndf_m2_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=43)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_m3_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=66)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_m4_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=87)).date().strftime('%Y-%m-%d %H:%M:%S')


def fixing_ndf_y1_front_end():
    return (tm(datetime.utcnow().isoformat()) + bd(n=261)).date().strftime('%Y-%m-%d %H:%M:%S')


def get_expire_time(ttl: int = 120):
    """
    Method can be used to get timestamp of quote expire time.
    it just return current time + quote time to live in FIX timestamp format
    """
    return (datetime.now() + timedelta(seconds=ttl)).strftime("%Y%m%d-%H:%M:%S.000")

# TODO need to add another tenors
