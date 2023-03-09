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
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.OrderQuoteFX import OrderQuoteFX
from test_framework.java_api_wrappers.fx.QuoteManualSettingsRequestFX import QuoteManualSettingsRequestFX
from test_framework.java_api_wrappers.fx.QuoteRequestActionRequestFX import QuoteRequestActionRequestFX


class QAP_T2442(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.verifier = Verifier(self.test_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.manual_settings_request = QuoteManualSettingsRequestFX(data_set=self.data_set)
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.java_api_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.java_quote = OrderQuoteFX()
        self.action_request = QuoteRequestActionRequestFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.account_id = self.data_set.get_client_tier_id_by_name('client_tier_id_3')
        self.symbol = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date_1w = self.data_set.get_settle_date_by_name("wk1")
        self.settle_type_1w = self.data_set.get_settle_type_by_name("wk1")
        self.settle_type_1w_java = self.data_set.get_settle_type_ja_by_name('wk1')
        self.currency = self.data_set.get_currency_by_name("currency_gbp")

        self.qty = random_qty(9)

        self.instrument = {
            "Symbol": self.symbol,
            "SecurityType": self.security_type_fwd
        }

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1w_java, "ClientTierID": self.account_id, "InstrSymbol": self.symbol})
        self.manual_settings_request.set_executable_off()
        self.java_api_manager.send_message(self.manual_settings_request)
        self.sleep(4)
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument,
                                                           SettlDate=self.settle_date_1w, SettlType=self.settle_type_1w,
                                                           OrderQty=self.qty)
        response = self.fix_manager_sel.send_quote_to_dealer_and_receive_response(self.quote_request, self.test_id)
        self.sleep(2)
        req_id = check_quote_request_id(self.quote_request)
        self.sleep(2)
        self.action_request.set_default_params(req_id).set_action_assign()
        self.java_api_manager.send_message(self.action_request)
        self.sleep(2)
        self.action_request.set_action_estimate()
        estimation_reply = self.java_api_manager.send_message_and_receive_response(self.action_request)
        self.java_quote.set_params_for_fwd(self.quote_request, estimation_reply[0])
        self.java_api_manager.send_message(self.java_quote)
        self.quote.set_params_for_dealer_fwd(self.quote_request)
        self.quote.remove_parameters(["OrigMDArrivalTime", "OrigMDTime", "OrigClientVenueID"])
        self.fix_verifier.check_fix_message(self.quote)
        next(response)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 3
        self.manual_settings_request.set_default_params().update_fields_in_component(
            "QuoteManualSettingsRequestBlock",
            {"Tenor": self.settle_type_1w_java, "ClientTierID": self.account_id, "InstrSymbol": self.symbol})
        self.java_api_manager.send_message(self.manual_settings_request)
        self.sleep(4)
        # endregion
