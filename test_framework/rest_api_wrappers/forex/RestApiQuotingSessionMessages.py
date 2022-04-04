from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiQuotingSessionMessages(RestApiMessages):

    def __init__(self, data_set=None):
        super().__init__('ModifyQuotingSession', data_set)

    def set_default_params_esp(self):
        self.parameters = {
            "MDUpdateType": "FUL",
            "ackOrder": "true",
            "clientQuoteIDFormat": "#20d",
            "concurrentlyActiveQuoteAge": 10,
            "quotingSessionClientClientTier":
            [
                {
                    "clientClientTierID": "GOLD",
                    "clientTierID": 4
                }
            ],
            "quotingSessionClientTier":
            [
                {
                    "broadcastClientClientTierID": "Gold_Day",
                    "clientTierID": 4
                }
            ],
            "quotingSessionClientTierInstrSymbol":
            [
                {
                    "broadcastClientClientTierID": "Gold_Day",
                    "clientTierID": 4,
                    "instrSymbol": "EUR/USD"
                },
                {
                    "broadcastClientClientTierID": "Gold_Day",
                    "clientTierID": 4,
                    "instrSymbol": "GBP/USD"
                }
            ],
            "quotingSessionID": 8,
            "quotingSessionName": "QSESPTH2",
            "supportMDRequest": "true",
            "tradingQuotingSession": "true",
            "updateInterval": 3000,
            "updateMDEntryID": "true"
        }
        self.message_type = 'ModifyQuotingSession'
        return self

    def set_default_params_rfq(self):
        self.parameters = {
            "MDUpdateType": "FUL",
            "ackOrder": "false",
            "clientQuoteIDFormat": "#20d",
            "concurrentlyActiveQuoteAge": 120000,
            "quotingSessionID": 10,
            "quotingSessionName": "QSRFQTH2",
            "supportMDRequest": "true",
            "tradingQuotingSession": "true",
            "updateInterval": 10000,
            "updateMDEntryID": "true"
        }
        self.message_type = 'ModifyQuotingSession'
        return self

    def set_update_type_incremental(self):
        self.parameters.update({"MDUpdateType": "INC"})
        return self

    def set_update_type_fullrefresh(self):
        self.parameters.update({"MDUpdateType": "FUL"})
        return self

    def enable_always_new_mdentryid(self):
        self.parameters.update({"updateMDEntryID": "true"})
        return self

    def disable_always_new_mdentryid(self):
        self.parameters.update({"updateMDEntryID": "false"})
        return self
