from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import random_qty, check_quote_request_id
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


class QAP_T2582(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.action_request = QuoteRequestActionRequestFX()
        self.qty_1m = random_qty(1, 2, 7)
        self.client_argentina = self.data_set.get_client_by_name("client_mm_2")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.sec_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.eur_gbp_fwd = {
            "Symbol": self.eur_gbp,
            "SecurityType": self.sec_type_fwd}
        self.settle_type_3w = self.data_set.get_settle_type_by_name("wk3")
        self.settle_date_3w = self.data_set.get_settle_date_by_name("wk3")

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_rfq_params_fwd().update_repeating_group_by_index(component="NoRelatedSymbols", index=0,
                                                                                Account=self.client_argentina,
                                                                                Instrument=self.eur_gbp_fwd,
                                                                                Currency=self.gbp,
                                                                                SettlDate=self.settle_date_3w,
                                                                                SettlType=self.settle_type_3w,
                                                                                OrderQty=self.qty_1m)
        response = self.fix_manager.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
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
        self.java_quote.set_params_for_fwd_ccy2(self.quote_request, estimation_reply[0])
        self.java_api_manager.send_message(self.java_quote)
        quote_response = next(response)
        quote_from_di = self.fix_manager.parse_response(quote_response)[0]
        self.quote.set_params_for_dealer_fwd_ccy2(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion
        # region Step 3

        self.new_order_single.set_default_for_dealer_ccy2(self.quote_request, quote_from_di)
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        # endregion

        # region Step 4
        self.execution_report.set_params_from_new_order_single_ccy2(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report,
                                            ignored_fields=["trailer", "header", "GatingRuleCondName",
                                                            "GatingRuleName"])
        # endregion
