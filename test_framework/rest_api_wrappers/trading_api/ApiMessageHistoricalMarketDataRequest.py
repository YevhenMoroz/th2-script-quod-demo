from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet


class ApiMessageHistoricalMarketDataRequest(TradingRestApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.HistoricalMarketDataRequest.value,
                         response_type_http=TradingRestApiMessageType.HistoricalMarketDataReply.value,
                         data_set=data_set)
        super().change_parameters(parameters)

    def set_default_request(self):
        base_parameters = {
            "StartTime": "2022-01-20T10:07:59.588Z",
            "EndTime": "2022-01-29T10:07:59Z",
            "Instrument": {'InstrSymbol': 'SPICEJET-IQ[NSE]',
                           'SecurityID': '11564',
                           'SecurityIDSource': 'EXC',
                           'InstrType': 'EQU',
                           }
        }
        super().change_parameters(base_parameters)

