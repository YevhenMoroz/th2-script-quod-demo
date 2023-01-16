from pathlib import Path
from custom import basic_custom_actions as bca
from stubs import Stubs
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX
from test_framework.rest_api_wrappers.RestApiManager import RestApiManager
from test_framework.rest_api_wrappers.forex.RestApiOrderVelocityMessages import RestApiOrderVelocityMessages


class QAP_T2463(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.fix_act = Stubs.fix_act
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.rest_api_connectivity = self.environment.get_list_web_admin_rest_api_environment()[0].session_alias_wa
        self.rest_manager = RestApiManager(self.rest_api_connectivity, self.test_id)
        self.fix_manager_gtw = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.velocity_rule = RestApiOrderVelocityMessages()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.execution_report_rej = FixMessageExecutionReportPrevQuotedFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.quote = FixMessageQuoteFX()
        self.client = self.data_set.get_client_by_name("client_mm_3")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type = self.data_set.get_security_type_by_name("fx_spot")
        self.currency_gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.settle_date_spo = self.data_set.get_settle_date_by_name("spot")
        self.msg_prams = None
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type
        }
        self.rest_message_params = None
        self.response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.velocity_rule.set_default_params().change_params({"accountGroupID": self.client,
                                                               "instrSymbol": self.gbp_usd
                                                               }).create_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
        self.sleep(3)

        self.velocity_rule.find_all_limits()
        self.rest_message_params = self.rest_manager.parse_create_response(
            self.rest_manager.send_get_request(self.velocity_rule))
        self.rest_message_params = self.rest_message_params["OrderVelocityLimitResponse"][0]
        limit_id = self.rest_message_params["orderVelocityLimitID"]
        # endregion
        # region Step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency_gbp,
                                                           Instrument=self.instrument,
                                                           OrderQty="500000")
        self.response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, self.response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
        # region Step 3
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.client,
                                                           Currency=self.currency_gbp,
                                                           Instrument=self.instrument)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.quote_request)
        self.quote.set_params_for_quote(self.quote_request)
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single)
        rejected = Status.Reject
        text = f"17568 Accumulated quantity of order creation/modification reached " \
               f"the limit 1000000 of 'OrderVelocityLimit' {limit_id}"
        self.execution_report_rej.set_params_from_new_order_single(self.new_order_single, status=rejected, text=text)
        self.execution_report_rej.add_tag({"OrdRejReason": "99"})
        self.execution_report_rej.remove_parameters(["LastMkt", "ExecRestatementReason", "SettlType", "SettlCurrency"])
        self.fix_verifier.check_fix_message(self.execution_report_rej)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.velocity_rule.clear_message_params().set_params(self.rest_message_params).delete_limit()
        self.rest_manager.send_post_request(self.velocity_rule)
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager_gtw.send_message(self.quote_cancel)
        self.sleep(2)
