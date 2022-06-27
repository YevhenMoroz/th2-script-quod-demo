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

    def delete_deviation_cleansing_ruler(self):
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

    def set_spot(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_spot")})

    def set_fwd(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_fwd")})

    def set_swap(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_swap")})

    def set_ndf(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_ndf")})

    def set_nds(self):
        self.update_parameters({'instrType': self.data_set.get_fx_instr_type_wa("fx_nds")})
