from enum import Enum


class MobileUsers(Enum):
    user_1 = "automation_mobile1"
    user_2 = ""
    user_3 = "quodsup"
    user_4 = "QA4"
    user_5 = "QA5"


class MobilePasswords(Enum):
    password_1 = "QuodNumber1="
    password_2 = ""
    password_3 = "quodsup"
    password_4 = "QA4"
    password_5 = "QA5"

class MobileClient(Enum):
    client_1 = "mobile_client1"
    client_2 = "mobile_client2"
    client_3 = "mobile_client3"
    client_4 = "mobile_client4"
    client_5 = "mobile_client5"

class MobileAccount(Enum):
    account_1_1 = "mobile1_account1"

    account_2_1 = "mobile2_account1"
    account_2_2 = "mobile2_account1"

    account_3_1 = "mobile3_account1"

    account_4_1 = "mobile4_account1"

    account_5_1 = "mobile5_account1"

class MobileCashAccount(Enum):
    cash_account_1_1 = "mobile1_cash1_INR"

    cash_account_2_1 = "mobile2_cash1_INR"

    cash_account_3_1 = "mobile3_cash1_INR"
    cash_account_3_2 = "mobile3_cash2_GBP"
    cash_account_3_3 = "mobile3_cash3_INR"

    cash_account_4_1 = "mobile4_cash1_INR"

    cash_account_5_1 = "mobile5_cash1_INR"

class MobileInstrument(Enum):
    instrument_1 = "TCS-IQ"
    instrument_2 = "SPICEJET-IQ"

class MobileOrderType(Enum):
    order_type_1 = "Limit"
    order_type_2 = "Market"
    order_type_3 = "Stop"
    order_type_4 = "StopLimit"

class MobileTimeInForce(Enum):
    time_in_force_1 = "Day"
    time_in_force_2 = "GoodTillCancel"
    time_in_force_3 = "GoodTillDate"
    time_in_force_4 = "FillOrKill"
    time_in_force_5 = "ImmediateOrCancel"