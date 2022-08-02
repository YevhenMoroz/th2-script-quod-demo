from pathlib import Path

from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.SessionAlias import SessionAliasFX
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2434(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.ss_connectivity = self.fix_env.sell_side_esp
        self.fix_manager_gtw = FixManager(self.ss_connectivity, self.test_id)
        self.fix_verifier = FixVerifier(self.ss_connectivity, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.account = self.data_set.get_client_by_name("client_mm_2")
        self.usd_sek = self.data_set.get_symbol_by_name('symbol_8')
        self.currency = self.data_set.get_currency_by_name("currency_usd")
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_date = self.data_set.get_settle_date_by_name("wk1")
        self.settle_type = self.data_set.get_settle_type_by_name("wk1")
        self.qty = "1000000"
        self.status_reject = Status.Reject
        self.instrument = {
            'Symbol': self.usd_sek,
            'SecurityType': self.security_type,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region step 1
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.account)
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)

        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        # endregion

        # region step 2
        self.new_order_single.set_default().change_parameters(
            {"Account": self.account, "Instrument": self.instrument,
             "SettlDate": self.settle_date, "SettlType": self.settle_type, "TimeInForce": "3", "OrdType": "1",
             "OrderQty": self.qty, "Currency":self.currency})
        self.new_order_single.remove_parameter("Price")
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)

        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.status_reject)
        self.execution_report.remove_parameters(["Price"])
        self.execution_report.add_tag({"LastMkt": "XQFX"})
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
