from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty, check_quote_request_id, check_quote_status
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX


class QAP_T2905(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.action_request = QuoteRequestActionRequestFX()
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.gbp_usd_spot = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_spot
        }
        self.qty = random_qty(5, 6, 8)
        self.db_column = "quoterequestid"
        self.quote_response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1-2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.gbp, Instrument=self.gbp_usd_spot,
                                                           OrderQty=self.qty)
        response = self.fix_manager_gtw.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_dealer(self.quote_request)
        self.sleep(2)
        req_id = check_quote_request_id(self.quote_request)
        self.sleep(2)
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_api_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_api_manager.send_message_and_receive_response(self.action_request)
        self.java_quote.set_params_for_quote(self.quote_request, estimation_reply[0])
        self.java_api_manager.send_message(self.java_quote)
        self.quote_response = next(response)
        self.quote.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        self.action_request.set_action_reject()
        self.java_api_manager.send_message(self.action_request)
        quote_status = check_quote_status(req_id, self.db_column)
        self.verifier.set_parent_id(self.test_id)
        self.verifier.set_event_name("Check quote status")
        self.verifier.compare_values("Quote removed from Market", quote_status, "REM")
        self.verifier.verify()
        # endregion
