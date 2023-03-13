from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportPrevQuotedFX import \
    FixMessageExecutionReportPrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSinglePrevQuotedFX import FixMessageNewOrderSinglePrevQuotedFX
from test_framework.fix_wrappers.forex.FixMessageQuoteFX import FixMessageQuoteFX
from test_framework.fix_wrappers.forex.FixMessageQuoteRequestFX import FixMessageQuoteRequestFX


class QAP_T10431(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.ss_rfq_connectivity = self.environment.get_list_fix_environment()[0].sell_side_rfq
        self.fix_manager_sel = FixManager(self.ss_rfq_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_rfq_connectivity, self.test_id)
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.quote_request = FixMessageQuoteRequestFX(data_set=self.data_set)
        self.quote = FixMessageQuoteFX()
        self.new_order_single = FixMessageNewOrderSinglePrevQuotedFX()
        self.execution_report = FixMessageExecutionReportPrevQuotedFX()
        self.account = self.data_set.get_client_by_name("client_mm_3")
        self.eur_gbp = self.data_set.get_symbol_by_name("symbol_3")
        self.security_type_spo = self.data_set.get_security_type_by_name("fx_spot")
        self.currency = self.data_set.get_currency_by_name("currency_eur")
        self.instrument = {
            "Symbol": self.eur_gbp,
            "SecurityType": self.security_type_spo
        }
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.md_req_id = self.eur_gbp + ":SPO:REG:" + self.hsbc

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step precondition
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(4)
        # endregion
        # region step 2
        self.quote_request.set_rfq_params()
        self.quote_request.update_repeating_group_by_index(component="NoRelatedSymbols", index=0, Account=self.account,
                                                           Currency=self.currency, Instrument=self.instrument)
        response: list = self.fix_manager_sel.send_message_and_receive_response(self.quote_request, self.test_id)
        self.quote.set_params_for_quote(quote_request=self.quote_request)
        # endregion
        # region Step 3
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        new_price = round(float(self.new_order_single.get_parameter("Price")) + 0.0002, 5)
        self.new_order_single.change_parameter("Price", new_price)
        self.fix_manager_sel.send_message(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, status=Status.Reject,
                                                               text="invalid price")
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
        # region Step 4
        self.new_order_single.set_default_prev_quoted(self.quote_request, response[0])
        self.fix_manager_sel.send_message(self.new_order_single)
        self.execution_report.set_params_from_new_order_single(self.new_order_single).remove_parameters(
            ["Text", "ExecRestatementReason"])
        self.fix_verifier.check_fix_message(self.execution_report)
        # endregion
