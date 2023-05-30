import time
from copy import deepcopy
from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiVenueMessages import RestApiVenueMessages


class QAP_T2387(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.venue_message = RestApiVenueMessages()
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.msg_prams_client = None
        self.venue = "HSBC"
        self.qty = "1000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.venue_message.find_venue(self.venue)
        self.msg_prams_client = self.rest_manager.send_get_request_filtered(self.venue_message)
        self.msg_prams_client = self.rest_manager.parse_response_details(self.msg_prams_client,
                                                                         {"venueID": self.venue})
        self.msg_prams_client_default = deepcopy(self.msg_prams_client)
        self.msg_prams_client.update({"quoteTTL": "50"})
        self.venue_message.clear_message_params().modify_venue().set_params(self.msg_prams_client)
        self.rest_manager.send_post_request(self.venue_message)
        time.sleep(2)
        # endregion
        self.quote_request.set_rfq_params()

        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                           OrderQty=self.qty, Account=self.account,
                                                           Instrument=self.instrument)
        self.fix_manager_sel.send_message_and_receive_response(self.quote_request)
        # endregion
        # region Step 3
        self.quote.set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion
        # region Step 4
        self.sleep(120)
        self.quote_cancel.set_params_for_receive(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote_cancel, key_parameters=["QuoteReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.venue_message.clear_message_params().modify_venue().set_params(self.msg_prams_client_default)
        self.rest_manager.send_post_request(self.venue_message)
        self.sleep(2)
