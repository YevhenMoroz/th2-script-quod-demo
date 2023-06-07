from test_framework.java_api_wrappers.mpas_messages.AutoHedgerInstrSymbolBatchUpdate import \
    AutoHedgerInstrSymbolBatchUpdate


class AutoHedgerInstrSymbolBatchUpdateFX(AutoHedgerInstrSymbolBatchUpdate):

    def __init__(self, parameters: dict = None):
        super().__init__(parameters)
        self.change_parameters(parameters)

    def set_default_params(self, ah_id, instr_symbol):
        base_parameters = {
            "AutoHedgerInstrSymbolBatchUpdateBlock": {
                "AutoHedgerInstrSymbolStatusList": {
                    "AutoHedgerInstrSymbolStatusBlock":
                        [
                            {
                                "AlgoPolicyID": "*",
                                "ScenarioID": "*",
                                "AutoHedgerScheduleStatus": "*",
                                "AutoHedgerID": ah_id,
                                "SendHedgeOrders": "*",
                                "StalledAutoHedger": "*",
                                "SysCurrRTQty": "*",
                                "InstrSymbol": instr_symbol,
                                "HedgeAccountGroupID": "*",
                                "TimeInForce": "*",
                                "HedgingStrategy": "*",
                                "AutoHedgerName": "*",
                                "HedgeOrderDestination": "*",
                                "PositQty": "*",
                                "LeavesQty": "*",
                            }
                        ]
                }

            }
        }
        return self.change_parameters(base_parameters)
