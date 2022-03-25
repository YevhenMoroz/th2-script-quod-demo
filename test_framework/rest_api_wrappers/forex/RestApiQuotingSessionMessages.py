from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiQuotingSession(RestApiMessages):

    def set_default_params(self):
        self.parameters = {
            "quotingSessionName": "QSESPTH2",
            "MDUpdateType": "FullRefresh",
            "updateMDEntryID": "true"
        }
        self.message_type = 'ModifyQuotingSession'
        return self

    def set_update_type_incremental(self):
        self.parameters.update({"MDUpdateType": "IncrementalRefresh"})
        return self

    def set_update_type_fullrefresh(self):
        self.parameters.update({"MDUpdateType": "FullRefresh"})
        return self

    def enable_always_new_mdentryid(self):
        self.parameters.update({"updateMDEntryID": "true"})
        return self

    def disable_always_new_mdentryid(self):
        self.parameters.update({"updateMDEntryID": "false"})
        return self
