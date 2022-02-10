from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage


class FixMessageMarketDataRequestReject(FixMessage):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.MarketDataRequestReject.value, data_set=data_set)
        super().change_parameters(parameters)
