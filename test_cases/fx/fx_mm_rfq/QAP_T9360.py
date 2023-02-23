from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import check_quote_request_id, extract_automatic_quoting, extract_freenotes
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX


class QAP_T9360(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment, )
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_rfq = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.quote_2 = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.action_request = QuoteRequestActionRequestFX()
        self.iridium = self.data_set.get_client_by_name("client_mm_3")
        self.quote_cancel = FixMessageQuoteCancelFX()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium,
                                                           QuoteRequestType="1")
        response = self.fix_manager_rfq.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # region Step 2
        self.sleep(2)
        automatic_quoting = extract_automatic_quoting(self.quote_request)
        free_notes = extract_freenotes(self.quote_request)
        req_id = check_quote_request_id(self.quote_request)
        expected_list = ["N", "quote request is explicitly manual"]
        actual = [automatic_quoting, free_notes]
        self.compare_values(self.test_id, expected_list, actual, event_name="Check Automating quoting and free notes")
        # endregion
        # Region Step 3
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_manager.send_message_and_receive_response(self.action_request)
        print(estimation_reply[-1].get_parameters())
        self.java_quote.set_params_for_quote(self.quote_request, estimation_reply[-1])
        self.java_manager.send_message(self.java_quote)
        self.quote.set_params_for_dealer(self.quote_request)
        self.quote.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        next(response)
        self.fix_verifier.check_fix_message(self.quote)
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.quote)
        self.fix_manager_rfq.send_message(self.quote_cancel)
        self.sleep(1)
        # endregion
        # region Step 4
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium,
                                                           QuoteRequestType="2")
        self.fix_manager_rfq.send_message_and_receive_response(self.quote_request)
        self.quote_2.set_params_for_quote(self.quote_request)
        self.fix_verifier.check_fix_message(self.quote)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.quote_2)
        self.fix_manager_rfq.send_message(self.quote_cancel)
