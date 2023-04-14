from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingCrossedReferenceRatesMessages(RestApiMessages):

    def find_all_cross_ref_rates_cleansing_rules(self):
        """
        Default message to get all Price Cleansing Crossed Reference Rates rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingCrossedReferenceRates'
        return self

    def modify_cross_ref_rates_cleansing_rule(self):
        self.message_type = 'ModifyPriceCleansingCrossedReferenceRates'
        return self

    def create_cross_ref_rates_cleansing_rule(self):
        if 'prcClnCrossedRefRatesID' in self.parameters.keys():
            self.remove_parameter('prcClnCrossedRefRatesID')
        self.message_type = 'CreatePriceCleansingCrossedReferenceRates'
        return self

    def delete_cross_ref_rates_cleansing_rule(self):
        """
        Default message to delete Crossed Reference Rates Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingCrossedReferenceRates'
        return self

    def set_default_params(self):
        self.parameters = {
            "alive": 'true',
            "instrSymbol": "GBP/USD",
            "instrType": "SPO",
            "prcClnCrossedRefRatesID": '2800033',
            "priceCleansingRuleName": "test",
            "venueID": "HSBC",
            "removeDetectedUpdate": 'true',
            "priceCleansingReferenceVenue": [
                {"venueID": "CITI"},
                {"venueID": "BARX"},
                {"venueID": "BNP"},
                {"venueID": "GS"}
            ],
        }
        return self

    def set_target_venue(self, venue_name):
        self.update_parameters({'venueID': venue_name})
        return self

    def set_ref_venues(self, venues: list):
        self.update_parameters({'priceCleansingReferenceVenue': venues})
        return self

    def clear_ref_venues(self):
        self.update_parameters({'priceCleansingReferenceVenue': []})
        return self

    def add_ref_venue(self, venue_name):
        self.parameters["priceCleansingReferenceVenue"].append({"venueID": venue_name})
        return self

    def remove_ref_venue_by_id(self, id):
        self.parameters["priceCleansingReferenceVenue"].pop(id)
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
