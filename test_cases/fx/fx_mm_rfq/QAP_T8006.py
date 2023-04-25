from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteCancel import FixMessageQuoteCancelFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T8006(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.quote_cancel = FixMessageQuoteCancelFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.iridium1 = self.data_set.get_client_by_name("client_mm_3")
        self.settle_date_broken = self.data_set.get_settle_date_by_name("broken_w2w3")
        self.settle_type_broken = self.data_set.get_settle_type_by_name("broken")
        self.gbp_usd = self.data_set.get_symbol_by_name("symbol_2")
        self.security_type_fwd = self.data_set.get_security_type_by_name("fx_fwd")
        self.gbp = self.data_set.get_currency_by_name("currency_gbp")
        self.instrument = {
            "Symbol": self.gbp_usd,
            "SecurityType": self.security_type_fwd
        }
        self.response = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.quote_request.set_rfq_params_fwd()
        self.quote_request.update_repeating_group_by_index("NoRelatedSymbols", 0, Account=self.iridium1,
                                                           Currency=self.gbp, Instrument=self.instrument,
                                                           SettlDate=self.settle_date_broken,
                                                           SettlType=self.settle_type_broken)
        self.response: list = self.fix_manager.send_message_and_receive_response(self.quote_request, self.test_id)

        self.quote.set_params_for_quote_fwd(quote_request=self.quote_request)
        self.fix_verifier.check_fix_message(fix_message=self.quote)
        # endregion
        # region Step 2
        self.new_order_single.set_default_prev_quoted(self.quote_request, self.response[0])
        self.fix_manager.send_message_and_receive_response(self.new_order_single)
        # endregion
        # region Step 3
        self.execution_report.set_params_from_new_order_single(self.new_order_single)
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.quote_cancel.set_params_for_cancel(self.quote_request, self.response[0])
        self.fix_manager.send_message(self.quote_cancel)
        self.sleep(2)
