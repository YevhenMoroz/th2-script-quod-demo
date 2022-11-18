from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.message_types import FIXMessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from custom import basic_custom_actions as bca


class FixMessageQuoteRequestFX(FixMessage):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(message_type=FIXMessageType.QuoteRequest.value, data_set=data_set)
        super().change_parameters(parameters)

    def set_rfq_params(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": self.get_data_set().get_client_by_name("client_mm_1"),
                "Side": "1",
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                },
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
                "SettlType": self.get_data_set().get_settle_type_by_name("spot"),
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                "QuoteType": "1",
                "OrderQty": "1000000",
                "OrdType": "D"
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self

    def set_rfq_params_fwd(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": self.get_data_set().get_client_by_name("client_mm_1"),
                "Side": "1",
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_fwd")
                },
                "SettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                "SettlType": self.get_data_set().get_settle_type_by_name("wk1"),
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                "QuoteType": "1",
                "OrderQty": "1000000",
                "OrdType": "D"
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self

    def set_swap_rfq_params(self):
        quote_request_swap_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": self.get_data_set().get_client_by_name("client_mm_1"),
                "Side": "1",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_swap")
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                        },
                        "LegSide": "2",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("spot"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("spot"),
                        "LegOrderQty": "1000000"
                    },
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_fwd")
                        },
                        "LegSide": "1",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("wk1"),
                        "LegOrderQty": "1000000"
                    }
                ]
            }
            ]
        }
        super().change_parameters(quote_request_swap_params)
        return self

    def set_swap_fwd_fwd(self):
        quote_request_swap_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": self.get_data_set().get_client_by_name("client_mm_1"),
                "Side": "1",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_swap")
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_fwd"),
                        },
                        "LegSide": "2",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("wk1"),
                        "LegOrderQty": "1000000"
                    },
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_fwd")
                        },
                        "LegSide": "1",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk2"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("wk2"),
                        "LegOrderQty": "1000000"
                    }
                ]
            }
            ]
        }
        super().change_parameters(quote_request_swap_params)
        return self

    def set_swap_ndf(self):
        quote_request_swap_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": self.get_data_set().get_client_by_name("client_mm_1"),
                "Side": "1",
                "Currency": self.get_data_set().get_currency_by_name("currency_usd"),
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_ndf_1"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_nds")
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_ndf_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_spot"),
                        },
                        "LegSide": "2",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("spo_ndf"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("spot"),
                        "LegOrderQty": "1000000"
                    },
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_ndf_1"),
                            "LegSecurityType": self.get_data_set().get_security_type_by_name("fx_ndf")
                        },
                        "LegSide": "1",
                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk1_ndf"),
                        "LegSettlType": self.get_data_set().get_settle_type_by_name("wk1"),
                        "LegOrderQty": "1000000"
                    }
                ]
            }
            ]
        }
        super().change_parameters(quote_request_swap_params)
        return self

    def update_near_leg(self, leg_symbol: str = None, leg_sec_type: str = None, leg_side: str = None,
                        settle_type: str = None, settle_date: str = None, leg_qty: str = None):
        if leg_symbol is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["InstrumentLeg"]["LegSymbol"] = leg_symbol
        if leg_sec_type is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["InstrumentLeg"]["LegSecurityType"] = leg_sec_type
        if leg_side is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSide"] = leg_side
        if settle_type is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlType"] = settle_type
        if settle_date is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegSettlDate"] = settle_date
        if leg_qty is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["LegOrderQty"] = leg_qty
        return self

    def update_far_leg(self, leg_symbol: str = None, leg_sec_type: str = None, leg_side: str = None,
                       settle_type: str = None, settle_date: str = None, leg_qty: str = None):
        if leg_symbol is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["InstrumentLeg"]["LegSymbol"] = leg_symbol
        if leg_sec_type is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["InstrumentLeg"]["LegSecurityType"] = leg_sec_type
        if leg_side is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSide"] = leg_side
        if settle_type is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlType"] = settle_type
        if settle_date is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegSettlDate"] = settle_date
        if leg_qty is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1]["LegOrderQty"] = leg_qty
        return self

    def remove_side_from_legs(self):
        self.get_parameter(["NoRelatedSymbols"][0]["NoLegs"][0]).remove({"LegSide": "2"})
        self.get_parameter(["NoRelatedSymbols"][0]["NoLegs"][1]).remove({"LegSide": "2"})

    def set_deposit_and_loan_param(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "ClOrdID": bca.client_orderid(14),
            "NumOfCompetitors": "1",
            "VenueType": "M",
            "InCompetition": "N",
            "NoRelatedSym": [{
                "Instrument": {
                    "Symbol": self.get_data_set().get_currency_by_name("currency_usd"),
                    "Product": "9"
                },
                "NoPartyIDs": [
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "1"
                    },
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "3"
                    }
                ],
                "SettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                "MaturityDate": self.get_data_set().get_settle_date_by_name("wk2"),
                "Side": "2",
                "DayCount": "30/360",
                "OrderQty": "1000000",
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self

    def set_early_redemption_params(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NumOfCompetitors": "1",
            "InCompetition": "N",
            "VenueType": "I",
            "NoRelatedSym": [{
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SymbolSfx": "SD/CD",
                    "SecurityType": "FOR",
                    "Product": "4"
                },
                "NoPartyIDs": [
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "1"
                    },
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "3"
                    }
                ],
                "SettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                "SettlDate2": self.get_data_set().get_settle_date_by_name("wk2"),
                "Side": "2",
                "Price": "1.18153",
                "OrderQty": "1000000",
                "OrderQty2": "1000000",
                "QuoteRequestType": "100",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self
