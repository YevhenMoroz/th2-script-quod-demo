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
                "Instrument": {
                    "Symbol": "GBP/USD",
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

    def update_near_leg(self, near_leg_params: dict):
        self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][0] = near_leg_params
        return self

    def update_far_leg(self, far_leg_params):
        self.get_parameter("NoRelatedSymbols")[0]["NoLegs"][1] = far_leg_params
        return self
