import math
import random
import re
from datetime import datetime
from random import randint
import psycopg2
from psycopg2 import Error
import paramiko as paramiko


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


def parse_qty_from_di(qty_from_dealer):
    """
    Take qty value from Dealer (23.34M EUR for example) and parse from it only decimals value (23.34)
    """
    result = re.match(r'\d+(.\d+)?', qty_from_dealer)
    return result.group(0)


def update_quod_settings(setting_value: str):
    """
    Update value in cell settingvalue for row AutoRFQClientPricingFallback
    in quod314 data base
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.42",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details

        cursor.execute(
            f"update quodsettings set settingvalue ='{setting_value}' where  settingkey= 'AutoRFQClientPricingFallback'")
        connection.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def clear_position():
    """
    Clear position on quod314
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.42",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details

        cursor.execute("DELETE FROM FXCURRPAIRPOSIT")
        connection.commit()
        cursor.execute("DELETE FROM FXCURRPOSIT")
        connection.commit()

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def restart_component_on_back():
    """
    Restart QS_RFQ_STANDARD_SELL component on quod314 backend
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("qrestart QUOD.QS_RFQ_FIX_TH2")
    for line in stdout.read().splitlines():
        print(line)
    stdin.close()


def restart_pks():
    """
    Restart QS_RFQ_STANDARD_SELL component on quod314 backend
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("qrestart QUOD.PKS")
    for line in stdout.read().splitlines():
        print(line)
    stdin.close()


def stop_fxfh():
    """
    Restart QS_RFQ_STANDARD_SELL component on quod314 backend
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("qstop -id QUOD.FXFH")
    for line in stdout.read().splitlines():
        print(line)
    stdin.close()


def start_fxfh():
    """
    Restart QS_RFQ_STANDARD_SELL component on quod314 backend
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("qstart FXFH")
    for line in stdout.read().splitlines():
        print(line)
    stdin.close()


def read_median_file():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("cat /home/quod314/mda/median_data.csv")
    list_of_values = []
    for line in stdout.read().splitlines():
        list_of_values.append(line)
    stdin.close()
    return str(list_of_values[-1])
