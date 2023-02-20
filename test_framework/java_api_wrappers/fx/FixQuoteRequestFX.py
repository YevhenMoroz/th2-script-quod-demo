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
        self.swap = False
        super().__init__(message_type=ORSMessageType.QuoteRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_rfq_params(self):
        self.swap = False
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
                            "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot"),
                            "Tenor": self.get_data_set().get_tenor_java_api_by_name("tenor_spot")
                        },
                        "QuoteType": "Tradeable",
                        "Side": "Buy",
                        "SettlType": self.get_data_set().get_settle_type_ja_by_name("spot"),
                        "SettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api"),
                        "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                        "OrdType": "PreviouslyQuoted",
                        "OrdQty": "1000000",
                        "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_3"),
                        "QuotingSessionID": "10",
                        "LiveQuoteID": bca.client_orderid(9),
                    }]
                }
            }
        }
        super().change_parameters(quote_request_params)
        return self

    def set_rfq_params_fwd(self):
        self.swap = False
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
                            "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_fwd"),
                            "Tenor": self.get_data_set().get_tenor_java_api_by_name("tenor_1w")
                        },
                        "QuoteType": "Tradeable",
                        "Side": "Buy",
                        "SettlType": self.get_data_set().get_settle_type_ja_by_name("wk1"),
                        "SettlDate": self.get_data_set().get_settle_date_by_name("wk1_java_api"),
                        "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                        "OrdType": "PreviouslyQuoted",
                        "OrdQty": "1000000",
                        "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_3"),
                        "QuotingSessionID": "10",
                        "LiveQuoteID": bca.client_orderid(9),
                    }]
                }
            }
        }
        super().change_parameters(quote_request_params)
        return self

    def set_rfq_params_swap(self):
        self.swap = True
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
                            "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_fwd"),
                        },
                        "QuoteReqInstrumentLegList": {
                            "QuoteReqInstrumentLegBlock": [
                                {"InstrumentLegBlock": {
                                    "LegInstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                                    "LegCurrency": self.get_data_set().get_currency_by_name("currency_eur"),
                                    "LegTenor": self.get_data_set().get_tenor_java_api_by_name("tenor_spot")},
                                    "LegOrderQty": "24456780",
                                    "LegSettlType": self.get_data_set().get_settle_type_ja_by_name("spot"),
                                    "LegSettlDate": self.get_data_set().get_settle_date_by_name("spot_java_api")},
                                {"InstrumentLegBlock": {
                                    "LegInstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                                    "LegCurrency": self.get_data_set().get_currency_by_name("currency_eur"),
                                    "LegTenor": self.get_data_set().get_tenor_java_api_by_name("tenor_1w")},
                                    "LegOrderQty": "24456780",
                                    "LegSettlType": self.get_data_set().get_settle_type_ja_by_name("wk1"),
                                    "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk1_java_api")}]},
                        "QuoteType": "Tradeable",
                        "Side": "Buy",
                        "SettlType": self.get_data_set().get_settle_type_ja_by_name("wk1"),
                        "SettlDate": self.get_data_set().get_settle_date_by_name("wk1_java_api"),
                        "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                        "OrdType": "PreviouslyQuoted",
                        "OrdQty": "1000000",
                        "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_3"),
                        "QuotingSessionID": "10",
                        "LiveQuoteID": bca.client_orderid(9),
                    }]
                }
            }
        }
        super().change_parameters(quote_request_params)
        return self

    def change_client(self, client):
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["ClientAccountGroupID"] = client
        return self

    def change_instr_symbol(self, symbol, currency):
        params = self.get_parameters()
        if self.swap is False:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["InstrumentBlock"][
                "InstrSymbol"] = symbol
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["Currency"] = currency
        else:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["InstrumentBlock"][
                "InstrSymbol"] = symbol
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["Currency"] = currency
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0]["InstrumentLegBlock"]["LegInstrSymbol"] = symbol
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1]["InstrumentLegBlock"]["LegInstrSymbol"] = symbol
        return self

    def change_qty(self, qty):
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["OrdQty"] = qty

    def change_side(self, side):
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["Side"] = side
