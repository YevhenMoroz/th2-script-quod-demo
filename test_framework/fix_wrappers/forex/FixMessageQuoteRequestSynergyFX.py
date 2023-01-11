from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class FixMessageQuoteRequestSynergyFX(FixMessageQuoteRequestFX):

    def __init__(self, parameters: dict = None, data_set: BaseDataSet = None):
        super().__init__(parameters, data_set)

    def set_rfq_synergy_params(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NumOfCompetitors": "1",
            "InCompetition": "N",
            "VenueType": "M",
            "NoRelatedSym": [{
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": "FOR",
                    "Product": "4"
                },
                "NoPartyIDs": [
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "1"
                    }
                ],
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
                "OrderQty": "1000000",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self

    def set_rfq_synergy_params_fwd(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NumOfCompetitors": "1",
            "InCompetition": "N",
            "VenueType": "M",
            "NoRelatedSym": [{
                "Instrument": {
                    "SymbolSfx": "1W",
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_1"),
                    "SecurityType": "FOR",
                    "Product": "4"
                },
                "NoPartyIDs": [
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "1"
                    }
                ],
                "SettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                "OrderQty": "1000000",
                "Currency": self.get_data_set().get_currency_by_name("currency_eur"),
            }
            ]
        }
        super().change_parameters(quote_request_params)
        return self

    def set_rfq_synergy_params_multileg(self):
        quote_request_params = {
            "QuoteReqID": bca.client_orderid(9),
            "NoRelatedSym": [{
                "Instrument": {
                    "Symbol": self.get_data_set().get_symbol_by_name("symbol_2"),
                    "SecurityType": self.get_data_set().get_security_type_by_name("fx_mleg"),
                    "SecuritySubType": "FXFWD",
                    "Product": "4"
                },
                "NoLegs": [
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_2"),
                            "LegSymbolSfx": self.get_data_set().get_symbol_by_name("symbol_2"),
                            "LegCurrency": self.get_data_set().get_currency_by_name("currency_gbp"),
                            "LegSide": "1",
                        },

                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk1"),
                        "LegQty": "1000000",
                        "LegRefID": bca.client_orderid(9)
                    },
                    {
                        "InstrumentLeg": {
                            "LegSymbol": self.get_data_set().get_symbol_by_name("symbol_2"),
                            "LegSymbolSfx": self.get_data_set().get_symbol_by_name("symbol_2"),
                            "LegCurrency": self.get_data_set().get_currency_by_name("currency_gbp"),
                            "LegSide": "1",
                        },

                        "LegSettlDate": self.get_data_set().get_settle_date_by_name("wk2"),
                        "LegQty": "1000000",
                        "LegRefID": bca.client_orderid(9)
                    }
                ],
                "NoPartyIDs": [
                    {
                        "PartyID": self.get_data_set().get_client_by_name("client_mm_10"),
                        "PartyIDSource": "D",
                        "PartyRole": "1"
                    }
                ],
                "SettlDate": self.get_data_set().get_settle_date_by_name("spot"),
                "OrderQty": "1000000",
                "Currency": self.get_data_set().get_currency_by_name("currency_gbp"),
            }
            ],
            "NumOfCompetitors": "1",
            "InCompetition": "N",
            "VenueType": "M",
        }
        super().change_parameters(quote_request_params)
        return self
