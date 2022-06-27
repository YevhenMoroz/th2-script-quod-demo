from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingStaleRatesMessages(RestApiMessages):

    def find_all_stale_cleansing_rules(self):
        """
        Default message to get all Price Cleansing Deviation rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingRateDeviation'
        return self

    def modify_stale_cleansing_rule(self):
        self.message_type = 'ModifyPriceCleansingRateDeviation'
        return self

    def create_stale_cleansing_rule(self):
        """
        This method sets up and default dictionary required to create new AutoHedger
        """
        if 'prcClnRateDeviationID' in self.parameters.keys():
            self.remove_parameter('prcClnRateDeviationID')
        self.message_type = 'CreatePriceCleansingRateDeviation'
        return self

    def delete_stale_cleansing_rule(self):
        """
        Default message to delete Deviation Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingRateDeviation'
        return self
