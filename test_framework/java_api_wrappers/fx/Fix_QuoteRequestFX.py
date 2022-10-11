from datetime import datetime
from pandas import Timestamp as tm
from pandas.tseries.offsets import BusinessDay as bd
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.fx_data_set.fx_data_set import FxDataSet
from test_framework.data_sets.message_types import ORSMessageType
from test_framework.java_api_wrappers.JavaApiMessage import JavaApiMessage
from custom import basic_custom_actions as bca


class FixQuoteRequestFX(JavaApiMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = FxDataSet()):
        super().__init__(message_type=ORSMessageType.QuoteRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_rfq_params(self):
        quote_request_params = {
            "SEND_SUBJECT": "QUOD.ORS.FIX",
            "REPLY_SUBJECT": "QUOD.FIX_REPLY.gtwquod9",
            "QuoteRequestBlock": {
                "ClientQuoteReqID": bca.client_orderid(9),
                "QuoteReqList": {
                    "QuoteReqBlock": [{
                        "InstrumentBlock": {
                            "InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                            "ProductType": "CURRENCY",
                            "InstrType": "FXSpot",
                            "Tenor": self.get_data_set().get_tenor_by_name("tenor_spot")
                        },
                        "QuoteType": "Tradeable",
                        "Side": "Buy",
                        "SettlType": "Regular",
                        "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                        "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                        "OrdType": "PreviouslyQuoted",
                        "OrdQty": "24456778",
                        "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_1"),
                        "QuotingSessionID": "10",
                        "LiveQuoteID": bca.client_orderid(9),
                    }]
                }

            }
        }
        #     "QuoteRequestBlock": {
        #         "ClientQuoteReqID": bca.client_orderid(9),
        #         "QuoteReqList": [
        #             {"QuoteReqBlock":{
        #                 "InstrumentBlock":{
        #                     {"InstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
        #      }}
        # ]}
        # "Account": self.get_data_set().get_client_by_name("client_mm_1"),
        # "Side": "1",
        # "Instrument": {
        #     "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
        #     "SecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
        # },
        # "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
        # "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
        # "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
        # "QuoteType": "1",
        # "OrderQty": "1000000",
        # "OrdType": "D"

        super().change_parameters(quote_request_params)
        return self
