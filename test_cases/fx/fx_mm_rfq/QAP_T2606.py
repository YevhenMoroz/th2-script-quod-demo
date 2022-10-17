import copy
from pathlib import Path
from custom import basic_custom_actions as bca
from test_cases.fx.fx_wrapper.common_tools import  check_quote_request_id
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
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX


class QAP_T2606(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote = FixMessageQuoteFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.client_tier_id = self.data_set.get_client_tier_id_by_name("client_tier_id_3")
        self.symbol = self.data_set.get_symbol_by_name("symbol_1")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.security_type_spot = self.data_set.get_security_type_by_name("fx_spot")
        self.action_request = QuoteRequestActionRequestFX()
        self.java_quote = OrderQuoteFX()
        self.pricing_request = QuoteAdjustmentRequestFX()
        self.pricing_request_on = QuoteAdjustmentRequestFX()
        self.qty = "2000000"
        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_spot
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Disable pricing
        self.pricing_request.set_defaults().update_fields_in_component("QuoteAdjustmentRequestBlock",
                                                                       {"InstrSymbol": self.symbol,
                                                                        "ClientTierID": self.client_tier_id})
        self.pricing_request_on = copy.deepcopy(self.pricing_request)
        self.pricing_request.disable_pricing_by_index(2).disable_pricing_by_index(3)
        self.sleep(2)
        self.java_api_manager.send_message(self.pricing_request)
        # endregion
        # region step 1
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.client,
                                                           Instrument=self.instrument, Currency=self.currency,
                                                           OrderQty=self.qty)
        response = self.fix_manager_sel.send_quote_to_dealer_and_receive_response(self.quote_request)
        # endregion
        # region Step 2
        req_id = check_quote_request_id(self.quote_request)
        self.sleep(2)
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_api_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_api_manager.send_message_and_receive_response(self.action_request)
        self.java_quote.set_params_for_quote(self.quote_request, estimation_reply[0])
        self.java_api_manager.send_message(self.java_quote)

        self.quote.set_params_for_dealer(self.quote_request)
        quote_response = next(response)
        quote_from_di = self.fix_manager_sel.parse_response(quote_response)[0]
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        self.new_order_single.set_default_for_dealer(self.quote_request, quote_from_di)
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.java_api_manager.send_message(self.pricing_request_on)
