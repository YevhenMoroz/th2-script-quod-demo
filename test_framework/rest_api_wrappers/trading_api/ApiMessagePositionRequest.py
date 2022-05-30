from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet


class ApiMessagePositionRequest(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.PositionRequest,
                         response_type_http=TradingRestApiMessageType.PositionReply,
                         message_type_web_socket=TradingRestApiMessageType.PositionReport.value,
                         data_set=data_set)
        super().change_parameters(parameters)