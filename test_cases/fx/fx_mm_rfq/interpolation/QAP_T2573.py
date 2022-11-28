from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderMultiLegFX import FixMessageNewOrderMultiLegFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T2573(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fh_connectivity = self.environment.get_list_fix_environment()[0].feed_handler
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager = FixManager(self.fix_env.sell_side_rfq, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_rfq, self.test_id)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderMultiLegFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)

        self.acc_argentina = self.data_set.get_client_by_name("client_mm_2")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.usd = self.data_set.get_currency_by_name("currency_usd")
        self.security_type_swap = self.data_set.get_security_type_by_name("fx_swap")
        self.settle_type_broken = self.data_set.get_settle_type_by_name("broken")
        self.settle_date_broken1 = self.data_set.get_settle_date_by_name("broken_1")
        self.settle_date_broken2 = self.data_set.get_settle_date_by_name("broken_2")
        self.qty_2m = "2000000"
        self.sell_side = '2'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.quote_request.set_swap_fwd_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0,
                                                           Account=self.acc_argentina,
                                                           Currency=self.usd)
        self.quote_request.update_near_leg(settle_type=self.settle_type_broken, settle_date=self.settle_date_broken1)
        self.quote_request.update_far_leg(settle_type=self.settle_type_broken, settle_date=self.settle_date_broken2,
                                          leg_qty=self.qty_2m)
        response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote_swap_ccy2(self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote, key_parameters=["QuoteReqID"])
        # endregion

        # region Step 2
        self.new_order_single.set_default_prev_quoted_swap_ccy2(self.quote_request, response[0], side=self.sell_side)
        self.fix_manager_sel.send_message_and_receive_response(self.new_order_single)

        self.execution_report.set_params_from_new_order_swap(self.new_order_single)
        self.execution_report.change_parameter("SettlCurrency", "EUR")
        self.fix_verifier.check_fix_message(self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion
