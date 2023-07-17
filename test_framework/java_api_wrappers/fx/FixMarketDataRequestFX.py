from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import MDAMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixMarketDataRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=MDAMessageType.FixMarketDataRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_default_taker_sub(self):
        md_request_params = {
            "SEND_SUBJECT": "QUOD.MDA.FIX",
            "REPLY_SUBJECT": f"MDQUOD.FIX_REPLY.marketdatath2",
            "MarketDataRequestBlock": {
                "MDReqList": {"MDReqBlock": [{"MDEntryType": "Bid"}, {"MDEntryType": "Offer"}]},
                "InstrumentMDReqList": {
                    "InstrumentMDReqBlock": [
                        {
                            "InstrumentBlock": {
                                "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                                "SecurityIDSource": "ExchSymb",
                                "ProductType": "CURRENCY",
                                "CFI": "CITI-SW",
                                "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot")
                            },
                            "MarketID": "CITI-SW"

                        }
                    ],
                },
                "MDReqID": f"EUR/USD:SPO:REG:CITI_{bca.client_orderid(3)}",
                "SubscriptionRequestType": "Subscribe",
                "MDUpdateType": "FullRefresh",
                "BookType": "PriceDepth",
            }
        }
        super().change_parameters(md_request_params)
        return self

    def unsubscribe(self):
        md_block = self.get_parameter("MarketDataRequestBlock")
        md_block["SubscriptionRequestType"] = "Unsubscribe"
