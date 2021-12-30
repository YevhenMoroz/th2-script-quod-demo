from custom.tenor_settlement_date import spo, wk1
from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from custom import basic_custom_actions as bca


class FixMessageQuoteRequestFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.QuoteRequest.value)
        super().change_parameters(parameters)

    def set_rfq_params(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": "CLIENT1",
                "Side": "1",
                "Instrument": {
                    "Symbol": "EUR/USD",
                    "SecurityType": "FXSPOT"
                },
                "SettlDate": spo(),
                "SettlType": "0",
                "Currency": "EUR",
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
                "Account": "Iridium1",
                "Side": "1",
                "Instrument": {
                    "Symbol": "GBP/USD",
                    "SecurityType": "FXFWD"
                },
                "SettlDate": wk1(),
                "SettlType": "W1",
                "Currency": "GBP",
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
                "Account": "Iridium1",
                "Side": "1",
                "OrderQty": "1000000",
                "Currency": "EUR",
                "Instrument": {
                    "Symbol": "EUR/USD",
                    "SecurityType": "FXSWAP"
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": "EUR/USD",
                            "LegSecurityType": "FXSPOT"
                        },
                        "LegSide": "2",
                        "LegSettlType": "0",
                        "LegSettlDate": spo(),
                        "LegOrderQty": "1000000"
                    },
                    {
                        "InstrumentLeg": {
                            "LegSymbol": "EUR/USD",
                            "LegSecurityType": "FXFWD"
                        },
                        "LegSide": "1",
                        "LegSettlType": "W1",
                        "LegSettlDate": wk1(),
                        "LegOrderQty": "1000000"
                    }
                ]
            }
            ]
        }
        super().change_parameters(quote_request_swap_params)
        return self

    def update_near_leg(self, leg_symbol: str = None, leg_sec_type: bool = False, leg_side: str = None,
                        settle_type: str = None, settle_date: str = None, leg_qty: str = None):
        if leg_symbol is not None:
            self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0]["InstrumentLeg"]["LegSymbol"] = leg_symbol
        if leg_sec_type:
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
