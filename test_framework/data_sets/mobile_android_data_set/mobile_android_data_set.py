from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.mobile_android_data_set.mobile_android_const_enum import *


class MobileDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    user = MobileUsers
    password = MobilePasswords
    client = MobileClient
    accounts = MobileAccount
    cash_account = MobileCashAccount
    instrument = MobileInstrument
    order_type = MobileOrderType
    time_in_force = MobileTimeInForce
    # index = MobileIndex