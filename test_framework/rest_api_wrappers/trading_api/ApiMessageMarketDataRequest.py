from test_framework.rest_api_wrappers.trading_api.TradingRestApiMessage import TradingRestApiMessage
from test_framework.data_sets.message_types import TradingRestApiMessageType
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca


class ApiMessageMarketDataRequest(TradingRestApiMessage):
    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(request_type_http=TradingRestApiMessageType.MarketDataRequest.value,
                         response_type_http=TradingRestApiMessageType.MarketDataReply.value,
                         message_type_web_socket=TradingRestApiMessageType.MarketDataSnapshotFullRefresh.value,
                         data_set=data_set)
        super().change_parameters(parameters)
        self.tested_instrument_md = self.data_set.get_trading_api_instrument_by_name("instrument_1")

    def set_default_request(self):
        md_params = {
            "MDReqID": bca.client_orderid(10),
            "SubscriptionRequestType": "Snapshot",
            "MDReqInstruments":
                [
                    {
                        "Instrument":
                            {
                                'InstrSymbol': self.tested_instrument_md["InstrSymbol"],
                                'SecurityID': self.tested_instrument_md[ "SecurityID"],
                                'SecurityIDSource': self.tested_instrument_md["SecurityIDSource"],
                                'InstrType': self.tested_instrument_md["InstrType"],
                                'SecurityExchange': self.tested_instrument_md["SecurityExchange"]
                            }
                    }
                ]
        }
        super().change_parameters(md_params)
