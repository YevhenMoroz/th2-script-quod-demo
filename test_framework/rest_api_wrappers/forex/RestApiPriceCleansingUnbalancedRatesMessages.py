from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingUnbalancedRatesMessages(RestApiMessages):

    def find_all_unbalanced_rates_rules(self):
        """
        Default message to get all Price Cleansing Deviation rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingUnbalancedRates'
        return self

    def modify_unbalanced_rates_rule(self):
        self.message_type = 'ModifyPriceCleansingUnbalancedRates'
        return self

    def create_unbalanced_rates_rule(self):
        """
        This method sets up and default dictionary required to create new AutoHedger
        """
        if 'prcClnUnbalancedRatesID' in self.parameters.keys():
            self.remove_parameter('prcClnUnbalancedRatesID')
        self.message_type = 'CreatePriceCleansingUnbalancedRates'
        return self

    def delete_unbalanced_rates_rule(self):
        """
        Default message to delete Deviation Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingUnbalancedRates'
        return self

    def set_default_params(self):
        self.parameters = {
            'alive': 'true',
            'instrSymbol': "GBP/USD",
            'instrType': "SPO",
            'prcClnUnbalancedRatesID': '2600014',
            'priceCleansingRuleName': "test",
            'removeDetectedUpdate': 'true',
            'venueID': "CITI"
        }
        return self

    def set_venue(self, venue_name):
        self.update_parameters({'venueID': venue_name})
        return self

    def set_symbol(self, symbol):
        self.update_parameters({'instrSymbol': symbol})
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
