from custom import basic_custom_actions
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import ReadLogMessageType
from test_framework.read_log_wrappers.ReadLogMessage import ReadLogMessage


class ReadLogMessageAlgo(ReadLogMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=ReadLogMessageType.Csv_Message.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_compare_message_for_check_the_currency_rate(self) -> ReadLogMessage:
        base_parameters = {
            "Currency": 'SEK',
            "Rate": '9.960000000'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_lis_amount(self) -> ReadLogMessage:
        base_parameters = {
            "Amount1": '1500',
            "Amount2": '1992000.000000000',
            "Venue": 'CHIXLIS'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_skips_lis_phase(self) -> ReadLogMessage:
        base_parameters = {
            "OrderID": '*',
            "Text": 'skipping LIS phase'
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_the_venue_was_suspended(self) -> ReadLogMessage:
        base_parameters = {
            "OrderID": "*",
            "VenueName": "Euronext Paris",
        }
        super().change_parameters(base_parameters)
        return self

    def set_compare_message_for_check_tags_5052_and_207_mapping(self) -> ReadLogMessage:
        base_parameters = {
            "SecurityExchange": "QDL1",
            "ClOrdID": "*",
            "ExternalStrategyName": "QA_Auto_SORPING_1",
        }
        super().change_parameters(base_parameters)
        return self
