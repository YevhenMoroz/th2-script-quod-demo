from custom.tenor_settlement_date import spo, wk1
from test_framework.fix_wrappers.DataSet import MessageType
from test_framework.fix_wrappers.FixMessage import FixMessage
from custom import basic_custom_actions as bca


class FixMessageQuoteRequestFX(FixMessage):

    def __init__(self, parameters: dict = None):
        super().__init__(message_type=MessageType.QuoteRequest.value)
        super().change_parameters(parameters)

    def set_rfq_params(self) -> FixMessage:
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

    def set_swap_rfq_params(self) -> FixMessage:
        quote_request_swap_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSymbols": [{
                "Account": "CLIENT1",
                "Side": "1",
                "Instrument": {
                    "Symbol": "EUR/USD",
                    "SecurityType": "FXSPOT"
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": "EUR/USD",
                            "LegSecurityType": "FXSPOT"
                        },
                        "LegSide": "1",
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
                        "LegSettlType": "0",
                        "LegSettlDate": wk1(),
                        "LegOrderQty": "1000000"
                    }
                ]
            }
            ]
        }
        super().change_parameters(quote_request_swap_params)
        return self
