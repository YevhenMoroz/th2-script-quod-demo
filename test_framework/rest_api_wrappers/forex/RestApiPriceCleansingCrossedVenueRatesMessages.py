from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingCrossedVenueRatesMessages(RestApiMessages):

    def find_all_cross_venue_rates_cleansing_rules(self):
        """
        Default message to get all Price Cleansing Crossed Venue Rates rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingCrossedRates'
        return self

    def modify_cross_venue_rates_cleansing_rule(self):
        self.message_type = 'ModifyPriceCleansingCrossedRates'
        return self

    def create_cross_venue_rates_cleansing_rule(self):
        if 'prcClnCrossedRatesID' in self.parameters.keys():
            self.remove_parameter('prcClnCrossedRatesID')
        self.message_type = 'CreatePriceCleansingCrossedRates'
        return self

    def delete_cross_venue_rates_cleansing_rule(self):
        """
        Default message to delete Crossed Venue Rates Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingCrossedRates'
        return self

    def set_default_params(self):
        self.parameters = {
            "alive": 'true',
            "instrSymbol": "GBP/USD",
            "instrType": "SPO",
            "prcClnCrossedRatesID": '2800033',
            "priceCleansingRuleName": "test",
            "venueID": "HSBC",
            "removeDetectedUpdate": 'true',
        }
        return self

    def set_target_venue(self, venue_name):
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
