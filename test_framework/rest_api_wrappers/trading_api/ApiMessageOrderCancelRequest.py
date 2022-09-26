from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet


class ApiMessageOrderCancel(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.OrderCancelRequest.value,
                         response_type_http=TradingRestApiMessageType.OrderCancelReply.value,
                         message_type_web_socket=TradingRestApiMessageType.OrderUpdate.value,
                         data_set=data_set)
        super().change_parameters(parameters)

    def set_cancellation_parameters(self, nos_response: dict, negative_case=None):
        cancellation_parameters = {
            'ClOrdID': nos_response['ClOrdID'],
            'TransactTime': nos_response['TransactTime']
        }
        if negative_case is not None:
            super().__init__(request_type_http=TradingRestApiMessageType.OrderCancelRequest.value,
                             response_type_http=TradingRestApiMessageType.OrderCancelReply.value,
                             message_type_web_socket=TradingRestApiMessageType.OrderCancelReject.value)
            super().change_parameters(cancellation_parameters)
        else:
            super().change_parameters(cancellation_parameters)

