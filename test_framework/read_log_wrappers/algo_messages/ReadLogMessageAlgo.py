from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ReadLogMessageType
from test_framework.read_log_wrappers.ReadLogMessage import ReadLogMessage


class ReadLogMessageAlgo(ReadLogMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=ReadLogMessageType.Csv_Message.value, data_set=data_set)
        super().change_parameters(parameters)