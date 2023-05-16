import math
import random
import re
import time
from datetime import datetime, timedelta
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


def random_qty(from_number: int, to_number: int = None, len: int = 7):
    if to_number is None:
        to_number = from_number + 1
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
                                      host="10.0.22.69",
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


def check_quote_request_id(quote_request):
    """
    Get QuoteRequestId from DB using quote_req_id from fix request
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        quote_req_id = quote_request.get_parameter("QuoteReqID")
        query = f"SELECT quoterequestid  FROM quoterequest WHERE clientquotereqid ='{quote_req_id}'"
        cursor.execute(query)
        response = cursor.fetchone()[0]
        print(f"Extraction is successful! QuoteReID is {response}.")
        return response
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def check_value_in_db(id_reference=None, key_parameter="clientquoteid", extracting_value="quotestatus", table="quote", query=None):
    """
    Get value from DB using quote_id from fix request
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        if not query:
            try:
                quote_id = id_reference.get_parameter("QuoteID")
            except AttributeError:
                quote_id = id_reference
            query = f"SELECT {extracting_value}  FROM {table} WHERE {key_parameter} ='{quote_id}'"
        cursor.execute(query)
        response = cursor.fetchone()[0]
        print(f"Extraction is successful! {extracting_value} is {response}.")
        return response
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def extract_freenotes(quote_request):
    """
    Get freenotes from DB using quote_req_id from fix request
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        quote_req_id = quote_request.get_parameter("QuoteReqID")
        query = f"SELECT freenotes FROM quoterequest WHERE clientquotereqid ='{quote_req_id}'"
        cursor.execute(query)
        response = cursor.fetchone()[0]
        print(f"\nExtraction is successful! FreeNotes is \"{response}\".\n")
        return response
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def extract_automatic_quoting(quote_request):
    """
    Get automaticquoting from DB using quote_req_id from fix request
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        quote_req_id = quote_request.get_parameter("QuoteReqID")
        query = f"SELECT automaticquoting FROM quoterequest WHERE clientquotereqid ='{quote_req_id}'"
        cursor.execute(query)
        response = cursor.fetchone()[0]
        print(f"\nExtraction is successful! AutomaticQuoting is \"{response}\".\n")
        return response
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def execute_db_command(*args):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
                                      port="5432",
                                      database="quoddb")
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        for command in args:
            cursor.execute(command)
            print(command, "is executed.")
            connection.commit()
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")




def generate_schedule(hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                      minutes_to_time=None, day: str = None):
    schedule_dict = {
        'scheduleFromTime': str((datetime.now() - timedelta(
            hours=hours_from_time if hours_from_time is not None else 0,
            minutes=minutes_from_time if minutes_from_time is not None else 0))
                                .timestamp()).split(".", 1)[0] + '000',
        'scheduleToTime': str((datetime.now() + timedelta(
            hours=hours_to_time if hours_to_time is not None else 0,
            minutes=minutes_to_time if minutes_to_time is not None else 0)).
                              timestamp()).split(".", 1)[0] + '000',
        'weekDay': day if day is not None else datetime.now().strftime("%a").upper()
    }
    return schedule_dict


def generate_schedule_list(hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                           minutes_to_time=None, days: list = None):
    schedule_dict_list = []
    for day in days:
        schedule_dict_list.append(
            generate_schedule(
                hours_from_time, hours_to_time, minutes_from_time, minutes_to_time, day)
        )
    return schedule_dict_list


def generate_schedule_excep(hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                            minutes_to_time=None, date: str = None):
    schedule_dict = {
        'scheduleFromTime': str((datetime.now() - timedelta(
            hours=hours_from_time if hours_from_time is not None else 0,
            minutes=minutes_from_time if minutes_from_time is not None else 0))
                                .timestamp()).split(".", 1)[0] + '000',
        'scheduleToTime': str((datetime.now() + timedelta(
            hours=hours_to_time if hours_to_time is not None else 0,
            minutes=minutes_to_time if minutes_to_time is not None else 0)).
                              timestamp()).split(".", 1)[0] + '000',
        'scheduleExceptionDate': date if date is not None else str(datetime.now().timestamp()).split(".", 1)[0] + '000'
    }
    return schedule_dict


def generate_schedule_excep_list(hours_from_time=None, hours_to_time=None, minutes_from_time=None,
                                 minutes_to_time=None, dates: list = None):
    schedule_dict_list = []
    for date in dates:
        schedule_dict_list.append(
            generate_schedule_excep(
                hours_from_time, hours_to_time, minutes_from_time, minutes_to_time, date)
        )
    return schedule_dict_list


def clear_position():
    """
    Clear position on quod314
    """
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(user="quod314prd",
                                      password="quod314prd",
                                      host="10.0.22.69",
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


def login_and_execute(script: str = None):
    commands = ['su - quod314', 'quod314', script]
    if script is True:
        commands.append(script)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "ostronov", "stronov1993")
    channel = ssh.invoke_shell()
    for command in commands:
        channel.send(command + '\n')
        while not channel.recv_ready():
            time.sleep(0.1)
        time.sleep(0.1)
        if commands.index(command) != 2:
            output = channel.recv(9999)
            print(output.decode('utf-8'))
            time.sleep(0.4)
        else:
            for i in range(3):
                output = channel.recv(9999)
                print(output.decode('utf-8'))
                time.sleep(0.4)
    channel.close()


def restart_qs_rfq_fix_th2():
    """
    Restart QUOD.QS_RFQ_FIX_TH2 component on quod314 backend
    """
    login_and_execute('qrestart QUOD.QS_RFQ_FIX_TH2')


def restart_pks():
    """
    Restart PKS component on quod314 backend
    """
    login_and_execute("qrestart QUOD.PKS")


def restart_mpas():
    """
    Restart MPAS component on quod314 backend
    """
    login_and_execute("qrestart QUOD.MPAS")

def stop_fxfh():
    """
    Stop FXFH component on quod314 backend
    """
    login_and_execute("qstop -id QUOD.FXFH")
    time.sleep(10)


def start_fxfh():
    """
    Start FXFH component on quod314 backend
    """
    login_and_execute("qstart FXFH")
    time.sleep(10)


def read_median_file():
    # TODO refactor method
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("10.0.22.34", 22, "quod314", "quod314")

    stdin, stdout, stderr = ssh.exec_command("cat /home/quod314/mda/median_data.csv")
    list_of_values = []
    for line in stdout.read().splitlines():
        list_of_values.append(line)
    stdin.close()
    return str(list_of_values[-1])


hash_green = 'iVBORw0KGgoAAAANSUhEUgAAAG4AAAAXCAIAAABlFO2lAAACK0lEQVR4Xu2X3UoCQRSAfa0Kooh+vSjUvOnPi5LoRiyJ3KKMAmm7iOyiH9QMsqtojVLb7nwEH2HfoDeos+N6GmdGC5rZCubjCMuZOQt+nJmdCbxrJBGAX0nzY7RKaWiVvcjdXqYezMVqJmrvRG0jVs1sWGbu7oqdR9AqxRRvrlOWGbLT4VeDiYhtrFfMwk2RKdEqBYDH1adDXiId8ecDxqZWKQD6kXfHR9I6oqu0ShbYH4XrGiN4tja8Eg3V0xF7+7R8gYXqVDacd+St+ciPOg0m59It7x/wneH10R77h8f7Bscmj+PhzsZUqrJt0LX6y4K+D3yvPXG2MXOfEnoc3VxsZRaqe1joi0qv19yM47yRNDNKcG1jnjw0vRGqq73JZIxvdgnM2jstjyOJuYHJ4HQ52c0jiW0s9EPlYxP10Y3qPXa2LK2ynadm4LD7TjUq4fwIjkK19NBSBMS1bHbxaMCuioVKVSKohO5Eqvs+jQjzvZOSibUXeKi25dmcmBJ6hJiv72KhUpXMXxWK+HMqN6iTENoUeoRIVnz+7Agy+Nxe/eycryY3qN1CKqflywhZ47RNoUeIk/I5Fv66ytYzbgO9VXp7JJnscO+XBtwLO5S9iI+ZiUqWrlKnUi1MM8sFboRwL+Td0bH8tJ8v/eeLIzalotWNgE04fsN9hpcYJv2YLxWYkn+m0mfgXghC4RwO50c498D3OmFl6f2RRquUhlYpDa1SGp5KjRQ+AOYYurVt0An0AAAAAElFTkSuQmCC'
hash_yellow = 'iVBORw0KGgoAAAANSUhEUgAAAG4AAAAXCAIAAABlFO2lAAACoklEQVR4Xu2YS2sTURSA+2MS2/hqwWprTZNpm8lGcNHYShaWLBTcqKAufGzciG1EXBQEK7bRUUoybTOjiAtxkZ0LN7HVVHQzShe+sChK4qaeeeTk9M4kCt6ZULgfNzBz7j2z+Dj3lY4NASc64JcT/DdCJTeEylYUlexyPv15qe+XFvlZjHwp9q0Ujuj3s+w4C6HSG+XunZV8uqqFf+shptW08Ct1XMndZlKESg/A43tVJu5CpycGj6akH4sNsx8WhxibQqUHUI+0DB9P9uyPJaHNXuyl8Yo6RrOEShZYH+m8/r4QPnRw2FY5kkh8nO/ELpjpD5WrmOifypKxgayXdXevUWJiJs3iwbFc2FSSM+f3gsTMWPxsJgoPkyf7ae/rQqMwfVVZN2habbOgfwf2azS19qBraEQGgy9u7nw3F4lKclRKvp3djgO+Lu3BxEBUOrVmRgxj3QozvRambYxbD2Wnh1S1M9jqcxc7B+DQg6YunxgAjxeOHbBfs6f64fVMJooDqvo2TAxCpV5GfbRQncfNJUtV1uNkBHab3/RZ5ctbOwbiyfiwbNzrsiOf5jsTcgJsPp/e5ajUwpjoq0oEldBKJNXXMOIZbx3kDJzDwVFNDx1Px8Da9Ll9WIPQ5i71QnDisFTVzNdvgU9wd8TTTrN46yBn4D4Djp5d77Z37WbtyVQPDFtVU5jYdpX12c+O+dvgElktuKIpU3DKKd3YPSiZG45ng83n6bVuUPlIuYKJbVdpP+My0Fqls0Zagw3X97lRUcfppG7WVvOjNMs/lf7CFDNf4EYI90K3O9rWFmJKboZmbTGVWJQ+zW4EbMK9sOb1dwa0N+oo4zG35VQGDNwL4T4D53A4P8K5B/brSiFF10eKUMkNoZIbQiU3HJUCLvwBzx3QB6pP6T4AAAAASUVORK5CYII='
hash_red = 'iVBORw0KGgoAAAANSUhEUgAAAG4AAAAXCAIAAABlFO2lAAACSklEQVR4Xu2Xz0sCURDH+7f6QZ3SU3XrEGmn0qAMslIRyxTM7mF16Af4D6QRBAXhnyCU6XE7VFCSN0EFm923O03vbRb0dkt4X57wdt7Mgh9mZ94MdJUkaQB+p0q/lkIpTQplL53tH96msq9riWYo1lyJ1Nc3K+lscf+Q9zOkUNorf3Jyl95tLW10liPcai9Hqqls/viYC1EobQQcH+IpESJdj7EkR1OhtBHkI+NVmgu+LIYpwfpi+MYfZPvq9g6NUih5QX1k3zVwHBnzzngmkSZw9Hmnhke91/4APLZD0WLuAAOdQ1nSuqhGuSCeaiXOpusru3u6TWcZOCAIHAdHPYwm4wiP0+MTz8FV5nNPEtNRlBZBneofA/q5oF/j50xpihxhvYXjGOgKSjPXdIumNQwzd2pIp412Y1M2T0hWm87GmZjsEtRciSEpSlPkCKsVimKgGygLZcRHE9Xcfk5ZitKyEw881t/pFMoPUh2rPjKUtG6aKJc2MNBRlChEQjORZN8HEVt7b6NkwT1c5Aj5SOsmOjTWEhjoKErur9qC+HcoK1bb4foM14WYT83ttmNjwb319fM+3zmXSLWQqkLuoG1guvIFhj7XR0YTjBez88xyvpfDwD9HyfZYBnqjNGuk4awJ75cmmAsZqUvfAtdngCZyrCUzNMo5lM6KS2a5gokQ5kJKUFxPkWT+6IhG9RlKTEqHvm4U0IS5EOYZEWLHyEeO42nfoXRZMBfCPAP3cLg/wr0H+nV1K0PrI5VCKU0KpTQplNJkolSSonfyFudeMKNRVgAAAABJRU5ErkJggg=='
