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
                            "InstrType": self.get_data_set().get_fx_instr_type_ja("fx_swap"),
                        },
                        "QuoteReqInstrumentLegList": {
                            "QuoteReqInstrumentLegBlock": [
                                {"InstrumentLegBlock": {
                                    "LegInstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                                    "LegInstrType": self.get_data_set().get_fx_instr_type_ja("fx_spot"),
                                    "LegCurrency": self.get_data_set().get_currency_by_name("currency_eur"),
                                    "LegTenor": self.get_data_set().get_tenor_java_api_by_name("tenor_spot")
                                },
                                    "LegOrderQty": "1000000",
                                    "LegSettlType": self.get_data_set().get_settle_type_ja_by_name("spot"),},
                                {"InstrumentLegBlock": {
                                    "LegInstrSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                                    "LegInstrType": self.get_data_set().get_fx_instr_type_ja("fx_fwd"),
                                    "LegCurrency": self.get_data_set().get_currency_by_name("currency_eur"),
                                    "LegTenor": self.get_data_set().get_tenor_java_api_by_name("tenor_1w")
                                },
                                    "LegOrderQty": "1000000",
                                    "LegSettlType": self.get_data_set().get_settle_type_ja_by_name("wk1"),}]},
                        "QuoteType": "Tradeable",
                        "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                        "QuoteRequestType": "Automatic",
                        "ClientAccountGroupID": self.get_data_set().get_client_by_name("client_mm_3"),
                        "QuotingSessionID": "10",
                    }]
                }
            }
        }
        super().change_parameters(quote_request_params)
        return self

    def change_client(self, client):
        """Tip: use client_mm for this method"""
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["ClientAccountGroupID"] = client
        return self

    def change_instr_symbol(self, symbol: str, currency: str, quote_currency: str = None):
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
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0]["InstrumentLegBlock"].update({"LegCurrency": currency})
        if quote_currency is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1]["InstrumentLegBlock"].update({"LegCurrency": quote_currency})
        return self

    def change_qty(self, qty):
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["OrdQty"] = qty

    def change_side(self, side):
        params = self.get_parameters()
        params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["Side"] = side

    def update_near_leg(self, settle_type: str = None, settle_date: str = None, leg_qty: str = None, tenor: str = None,
                        instr_type: str = None):
        params = self.get_parameters()
        if settle_type is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0].update({"LegSettlType": settle_type})
        if settle_date is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0].update({"LegSettlDate": settle_date})
        if leg_qty is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0].update({"LegOrderQty": leg_qty})
        if instr_type is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0]["InstrumentLegBlock"].update({"LegInstrType": instr_type})
        if tenor is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][0]["InstrumentLegBlock"].update({"LegTenor": tenor})
        return self

    def update_far_leg(self, settle_type: str = None, settle_date: str = None, leg_qty: str = None, tenor: str = None,
                       instr_type: str = None):
        params = self.get_parameters()
        if settle_type is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1].update({"LegSettlType": settle_type})
        if settle_date is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1].update({"LegSettlDate": settle_date})
        if leg_qty is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1].update({"LegOrderQty": leg_qty})
        if instr_type is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1]["InstrumentLegBlock"].update({"LegInstrType": instr_type})
        if tenor is not None:
            params["QuoteRequestBlock"]["QuoteReqList"]["QuoteReqBlock"][0]["QuoteReqInstrumentLegList"][
                "QuoteReqInstrumentLegBlock"][1]["InstrumentLegBlock"].update({"LegTenor": tenor})
        return self
