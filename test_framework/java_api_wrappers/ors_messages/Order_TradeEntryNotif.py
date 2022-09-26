from datetime import datetime

from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage


class Order_TradeEntryNotif(JavaApiMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=ORSMessageType.TradeEntryNotif.value)
        super().change_parameters(parameters)

    def set_default(self) -> None:
        base_parameters = {
            'TradeEntryNotifBlock': {}
        }
        super().change_parameters(base_parameters)
