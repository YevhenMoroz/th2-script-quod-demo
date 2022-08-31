from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet


class ApiMessageOrderModification(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.OrderModificationRequest.value,
                         response_type_http=TradingRestApiMessageType.OrderModificationReply.value,
                         message_type_web_socket=TradingRestApiMessageType.OrderUpdate.value,
                         data_set=data_set)
        super().change_parameters(parameters)
        self.default_instrument_nos = self.data_set.get_trading_api_instrument_by_name("instrument_2")

    def set_modification_parameters(self, nos_response: dict, new_parameters: dict, instrument=None, negative_case=None):
        modification_parameters = {
            'ClOrdID': nos_response['ClOrdID'],
            'Side': nos_response['Side'],
            'OrdType': nos_response['OrdType'],
            'ClientAccountGroupID': nos_response['ClientAccountGroupID'],
            'OrdQty': nos_response['OrdQty'],
            'Instrument': instrument if instrument is not None else self.default_instrument_nos,
            'Price': nos_response['Price'],
            'SettlCurrency': nos_response['SettlCurrency'],
            'PreTradeAllocations': [
                {
                    'AllocClientAccountID': nos_response['AllocClientAccountID'],
                    'AllocQty': nos_response['OrdQty']
                }
            ],
        }
        for key, value in new_parameters.items():
            if key == 'OrdQty':
                modification_parameters.update({'OrdQty': value})
                modification_parameters['PreTradeAllocations'][0].update({'AllocQty': value})
            modification_parameters.update({key: value})
        if negative_case is not None:
            super().__init__(request_type_http=TradingRestApiMessageType.OrderModificationRequest.value,
                             response_type_http=TradingRestApiMessageType.OrderModificationReply.value,
                             message_type_web_socket=TradingRestApiMessageType.OrderModificationReject.value)
            super().change_parameters(modification_parameters)
        else:
            super().change_parameters(modification_parameters)

