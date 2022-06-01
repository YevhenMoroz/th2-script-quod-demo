from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet


class ApiMessageOrderArchiveMassStatusRequest(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.OrderArchiveMassStatusRequest.value,
                         response_type_http=TradingRestApiMessageType.OrderArchiveMassStatusRequestReply.value,
                         data_set=data_set)
        super().change_parameters(parameters)

    def set_default_request(self):
        base_parameters = {'URI': {
            "StartTime": "2022-04-28T00:00:00",
            "EndTime": "2022-04-29T23:59:59"
        }}
        super().change_parameters(base_parameters)
