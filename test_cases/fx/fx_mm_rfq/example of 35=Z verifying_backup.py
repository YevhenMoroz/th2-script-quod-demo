class Test_UI(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.dealer_window = FXDealerIntervention(self.test_id, self.session_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.party = RFQPanelHeaderValues.party_value_label_control
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument_spot = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.qty = "1000000"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        quote_request = FixMessageQuoteRequestFX(data_set=self.data_set).set_rfq_params()
        quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                      Currency=self.currency, Instrument=self.instrument_spot,
                                                      OrderQty=self.qty)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(quote_request, self.test_id)
        quote = FixMessageQuoteFX().set_params_for_quote(quote_request)
        self.fix_verifier.check_fix_message(fix_message=quote, key_parameters=["QuoteReqID"])
        time.sleep(120)
        quote_cancel = FixMessageQuoteCancelFX().set_params_for_cancel(quote_request)

        self.fix_verifier.check_fix_message(fix_message=quote_cancel, key_parameters=["QuoteReqID"])