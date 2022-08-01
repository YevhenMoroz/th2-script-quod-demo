from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca


class ApiMessagePositionRequest(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.PositionRequest.value,
                         response_type_http=TradingRestApiMessageType.PositionReply.value,
                         message_type_web_socket=TradingRestApiMessageType.PositionReport.value,
                         data_set=data_set)
        super().change_parameters(parameters)
        self.default_client_positions = self.data_set.get_client_by_name('client_4')

    def set_default_request(self, client=None):
        base_positions_params = {
            "ClientAccountGroupID": client if client is not None else self.default_client_positions,
            "ClientPosReqID": bca.client_orderid(9),
            "PosReqType": "Positions",
            "SubscriptionRequestType": "Snapshot",
        }
        super().change_parameters(base_positions_params)