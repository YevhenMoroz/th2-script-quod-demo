import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_cases.fx.fx_wrapper.common_tools import random_qty, check_quote_request_id
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX
from test_framework.win_gui_wrappers.fe_trading_constant import QuoteRequestBookColumns
from test_framework.win_gui_wrappers.forex.fx_dealer_intervention import FXDealerIntervention


class QAP_T2564(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_2")
        self.symbol = self.data_set.get_symbol_by_name("symbol_3")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.action_request = QuoteRequestActionRequestFX()
        self.qty = random_qty(5, len=8)

        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_swap
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_near_leg(leg_symbol=self.symbol, leg_qty=self.qty)
        self.quote_request.update_far_leg(leg_symbol=self.symbol, leg_qty=self.qty)
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        response = self.fix_manager_sel.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        # endregion
        # region Step 2
        self.sleep(2)
        req_id = check_quote_request_id(self.quote_request)
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_manager.send_message_and_receive_response(self.action_request)
        print(estimation_reply[-1].get_parameters())
        self.java_quote.set_params_for_swap(self.quote_request, estimation_reply[-1])
        self.java_manager.send_message(self.java_quote)
        # endregion
        # region Step 3
        self.quote.set_params_for_dealer_swap(self.quote_request)
        # self.quote.remove_parameters(["QuoteType", "Side", "OfferPx"])
        quote_response = next(response)
        quote_from_di = self.fix_manager_sel.parse_response(quote_response)[0]
        self.fix_verifier.check_fix_message(self.quote)
        self.new_order_single.set_default_for_dealer_swap(self.quote_request, quote_from_di, side="1")
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_swap(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["header", "trailer", "GatingRuleCondName",
                                                            "GatingRuleName"])
        # endregion
