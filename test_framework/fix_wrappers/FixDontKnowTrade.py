from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage


class FixDontKnowTrade(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.DontKnowTrade.value, data_set=data_set)
        super().change_parameters(parameters)
        self.data_set = data_set

    def set_default(self, exec_id) -> None:
        base_parameters = {
            'ExecID': exec_id,
            "Instrument": self.get_data_set().get_fix_instrument_by_name("instrument_1"),
        }
        super().change_parameters(base_parameters)

