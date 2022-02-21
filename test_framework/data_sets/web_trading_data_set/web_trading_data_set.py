from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.web_trading_data_set.web_trading_const_enum import WebTradingUsers, WebTradingPasswords


class WebTradingDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    user = WebTradingUsers
    password = WebTradingPasswords
