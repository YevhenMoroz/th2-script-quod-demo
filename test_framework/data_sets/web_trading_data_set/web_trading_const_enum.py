from enum import Enum


class WebTradingUsers(Enum):
    user_1 = "QA1"
    user_2 = "user_desk"
    user_3 = "web_trading_test1"
    user_4 = "web_trading_test3"

class WebTradingPasswords(Enum):
    password_1 = "QA1"
    password_2 = "user_desk"
    password_3 = "Web1_trading_test"
    password_4 = "Web3_trading_test"


class WebTradingSymbol(Enum):
    symbol_1 = "AADIIND-Z  "



class WebTradingOrderType(Enum):
    order_type_1 = " Limit "


class WebTradingTimeInForce(Enum):
    time_in_force_1 = "Day "

class WebTradingClient(Enum):
    client_1 = "test_QAP_6286"
    client_2 = "POOJA"

class WebTradingInstrument(Enum):
    instrument_1 = "VALECHAENG-RL"

class WebTradingAccount(Enum):
    account_1 = "POOJA"