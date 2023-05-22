from test_framework.rest_api_wrappers.RestApiMessages import RestApiMessages


class RestApiPriceCleansingDeviationMessages(RestApiMessages):

    def find_all_deviation_cleansing_rules(self):
        """
        Default message to get all Price Cleansing Deviation rules
        """
        self.clear_message_params()
        self.message_type = 'FindAllPriceCleansingRateDeviation'
        return self

    def modify_deviation_cleansing_rule(self):
        self.message_type = 'ModifyPriceCleansingRateDeviation'
        return self

    def create_deviation_cleansing_rule(self):
        """
        This method sets up and default dictionary required to create new AutoHedger
        """
        if 'prcClnRateDeviationID' in self.parameters.keys():
            self.remove_parameter('prcClnRateDeviationID')
        self.message_type = 'CreatePriceCleansingRateDeviation'
        return self

    def delete_deviation_cleansing_rule(self):
        """
        Default message to delete Deviation Cleansing rule
        """
        self.message_type = 'DeletePriceCleansingRateDeviation'
        return self

    def set_exact_price_deviation_format(self):
        """
        Method sets an ExactPrice deviation format for the  cleansing rule
        """
        self.update_parameters({'priceDeviationFormat': 'EXA'})
        return self

    def set_pip_precision_deviation_format(self):
        """
        Method sets an FxPipPrecision deviation format for the rule
        """
        self.update_parameters({'priceDeviationFormat': 'PIP'})
        return self

    def set_default_params(self):
        self.parameters = {
            "priceCleansingRuleName": "test",
            "prcClnRateDeviationID": '2000009',
            "instrSymbol": "GBP/USD",
            "instrType": "SPO",
            "venueID": "HSBC",
            "removeDetectedUpdate": 'true',
            "priceDeviation": '0.00001',
            "priceDeviationFormat": "EXA",
            'priceDeviationRefPrice': "BAA",
            "priceCleansingReferenceVenue": [
                {"venueID": "CITI"},
                {"venueID": "BARX"},
                {"venueID": "BNP"},
                {"venueID": "GS"}
            ],
            "alive": 'true'
        }
        return self

    def set_target_venue(self, venue_name):
        self.update_parameters({'venueID': venue_name})
        return self

    def set_mid(self):
        self.update_parameters({'priceDeviationRefPrice': "MID"})
        return self

    def set_bid_and_ask(self):
        self.update_parameters({'priceDeviationRefPrice': "BAA"})
        return self

    def set_ref_venues(self, venues: list):
        self.update_parameters({'priceCleansingReferenceVenue': venues})
        return self

    def clear_ref_venues(self):
        self.update_parameters({'priceCleansingReferenceVenue': []})
        return self

    def add_ref_venues(self, venue_names: tuple):
        for i in venue_names:
            self.parameters["priceCleansingReferenceVenue"].append({"venueID": i})
        return self

    def remove_ref_venue_by_id(self, id):
        self.parameters["priceCleansingReferenceVenue"].pop(id)
        return self

    def set_symbol(self, symbol):
        self.update_parameters({'instrSymbol': symbol})
        return self

    def set_deviation(self, deviation):
        self.update_parameters({'priceDeviation': deviation})
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
