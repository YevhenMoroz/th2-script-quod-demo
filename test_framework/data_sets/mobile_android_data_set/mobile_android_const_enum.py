from enum import Enum


class MobileUsers(Enum):
    user_1 = "adm04"
    user_2 = ""
    user_3 = "quodsup"
    user_4 = "QA4"
    user_5 = "QA5"


class MobilePasswords(Enum):
    password_1 = "adm04"
    password_2 = ""
    password_3 = "quodsup"
    password_4 = "QA4"
    password_5 = "QA5"

class MobileClient(Enum):
    client_1 = "test_mobile_client"
    client_2 = "test_client"
    client_3 = "POOJA"

class MobileAccount(Enum):
    account_1 = "test_mobile_account"
    account_2 = "test_mobile_account2"
    account_3 = "test_account"
    account_4 = "test_account_1083"

class MobileCashAccount(Enum):
    cash_account_1 = "cash_account_mobile_INR"
    cash_account_2 = "test_cash_account"
    cash_account_3 = "IR_Cash_Account"

class MobileInstrument(Enum):
    instrument_1 = "TCS-IQ"
    instrument_2 = "SPICEJET-IQ"

class MobileOrderType(Enum):
    order_type_1 = "Limit"
    order_type_2 = "Market"

class MobileTimeInForce(Enum):
    time_in_force_1 = "Day"
    time_in_force_2 = "GoodTillCancel"
    time_in_force_3 = "GoodTillDate"
    time_in_force_4 = "FillOrKill"
    time_in_force_5 = "FillAndKill"

# class MobileIndex(Enum):
#     index_1 = "TASI"