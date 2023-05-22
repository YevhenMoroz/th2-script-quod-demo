from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty, check_quote_request_id, check_value_in_db
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


class QAP_T2863(TestCase):
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
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_gbp")
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.action_request = QuoteRequestActionRequestFX()
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.instrument_spot = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }
        self.qty = random_qty(5, 6, 8)

        self.quote_response = None
        self.verifier = Verifier(self.test_id)
        self.expected_free_notes = "11629 Quote is already in a terminal state"

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument_spot,
                                                           OrderQty=self.qty, Side="2")
        response = self.fix_manager_gtw.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_dealer(self.quote_request)
        self.sleep(2)
        req_id = check_quote_request_id(self.quote_request)
        # endregion
        # region Step 2
        self.sleep(2)
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_api_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_api_manager.send_message_and_receive_response(self.action_request)
        self.java_quote.set_params_for_quote(self.quote_request, estimation_reply[0])
        # self.java_api_manager.send_message(self.java_quote)
        self.java_quote.get_parameters()["QuoteBlock"]["QuoteTTL"] = "1"
        self.java_api_manager.send_message(self.java_quote)
        self.quote_response = next(response)
        quote_from_di = self.fix_manager_gtw.parse_response(self.quote_response)[0]
        self.quote.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        quote_req_id = check_quote_request_id(self.quote_request)
        quote_ttl = check_value_in_db(quote_req_id, "quoterequestid", "quotettl")
        self.verifier.set_event_name("Check modified bid (Java Quote message)")
        self.verifier.compare_values("QuoteTTL", "1", str(quote_ttl))
        self.verifier.verify()
        # endregion
        # region Step 3
        self.sleep(1)
        new_order_single = FixMessageNewOrderSinglePrevQuotedFX().set_default_for_dealer(self.quote_request,
                                                                                         quote_from_di)
        exec_report = self.fix_manager_gtw.send_message_and_receive_response(new_order_single)[-1].get_parameters()
        actual_free_notes = exec_report["Text"]
        self.verifier.set_event_name("Check FreeNotes (NewOrderSingle message)")
        self.verifier.compare_values("QuoteTTL", self.expected_free_notes, actual_free_notes)
        self.verifier.verify()
        # endregion
