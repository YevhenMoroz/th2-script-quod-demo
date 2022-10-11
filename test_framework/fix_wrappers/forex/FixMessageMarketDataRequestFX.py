from datetime import datetime

from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.fix_wrappers.FixMessageMarketDataRequest import FixMessageMarketDataRequest
from custom import basic_custom_actions as bca


class FixMessageMarketDataRequestFX(FixMessageMarketDataRequest):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(data_set=data_set)
        super().change_parameters(parameters)

    def set_md_req_parameters_maker(self) -> FixMessageMarketDataRequest:
        md_req_parameters = {
            "SenderSubID": self.get_data_set().get_client_by_name("client_mm_1"),
            "MDReqID": bca.client_orderid(10),
            "MarketDepth": "0",
            "MDUpdateType": "0",
            "SubscriptionRequestType": "1",
            "BookType": "0",
            "NoMDEntryTypes": [
                {"MDEntryType": "0"},
                {"MDEntryType": "1"}],
            "NoRelatedSymbols": [
                {
                    "Instrument": {
                        "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                        "SecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                        "Product": "4"
                    },
                    "SettlType": self.get_data_set().get_settle_type_by_name("spot")
                }
            ]
        }
        super().change_parameters(md_req_parameters)
        return self

    def set_md_uns_parameters_maker(self) -> FixMessageMarketDataRequest:
        self.change_parameters({"SubscriptionRequestType": "2"})
        return self

    def set_md_req_parameters_taker(self) -> FixMessageMarketDataRequest:
        md_req_parameters = {
            "MDReqID": "EUR/USD:SPO:REG:CITI_132",
            "MarketDepth": "0",
            "MDUpdateType": "0",
            "SubscriptionRequestType": "1",
            "BookType": "0",

            "NoMDEntryTypes": [
                {"MDEntryType": "0"},
                {"MDEntryType": "1"}],
            "NoRelatedSymbols": [
                {
                    "Instrument": {
                        "SecurityIDSource": "8",
                        "CFICode": "CITI-SW",
                        "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                        "SecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                        "Product": "4",

                    },
                    "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
                    "MarketID": "CITI-SW"
                }
            ],

        }
        super().change_parameters(md_req_parameters)
        return self
