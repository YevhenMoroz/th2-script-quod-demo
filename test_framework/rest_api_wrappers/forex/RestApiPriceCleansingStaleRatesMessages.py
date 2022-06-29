from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingStaleRatesMessages(RestApiMessages):

    def find_all_stale_cleansing_rules(self):
        """
        Default message to get all Price Cleansing Deviation rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingStaleRates'
        return self

    def modify_stale_cleansing_rule(self):
        self.message_type = 'ModifyPriceCleansingStaleRates'
        return self

    def create_stale_cleansing_rule(self):
        """
        This method sets up and default dictionary required to create new AutoHedger
        """
        if 'prcClnStaleRatesID' in self.parameters.keys():
            self.remove_parameter('prcClnStaleRatesID')
        self.message_type = 'CreatePriceCleansingStaleRates'
        return self

    def delete_stale_cleansing_rule(self):
        """
        Default message to delete Deviation Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingStaleRates'
        return self

    def set_default_params(self):
        self.parameters = {
            'alive': 'true',
            'instrSymbol': "GBP/USD",
            'instrType': "SPO",
            'prcClnStaleRatesID': '1600007',
            'priceCleansingRuleName': "test",
            'removeDetectedUpdate': 'true',
            'staleRatesDelay': '1',
            'venueID': "CITI"
        }
        return self

    def set_venue(self, venue_name):
        self.update_parameters({'venueID': venue_name})
        return self

    def set_symbol(self, symbol):
        self.update_parameters({'instrSymbol': symbol})
        return self

    def set_delay(self, delay):
        self.update_parameters({'staleRatesDelay': delay})
        return self

    def set_spot(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_spot")})
        return self

    def set_fwd(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_fwd")})
        return self

    def set_swap(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_swap")})
        return self

    def set_ndf(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_ndf")})
        return self

    def set_nds(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_nds")})
        return self
