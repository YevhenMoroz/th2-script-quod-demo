from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import Status, DirectionEnum
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshBuyFX import \
    FixMessageMarketDataSnapshotFullRefreshBuyFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2460(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh = FixManager(self.fix_env.feed_handler, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.execution_report_doubler = FixMessageExecutionReportFX()
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type_fwd = self.data_set.get_security_type_by_name('fx_fwd')
        self.settle_date_1w = self.data_set.get_settle_date_by_name('wk1')
        self.settle_type_1w = self.data_set.get_settle_type_by_name('wk1')
        self.bands_eur_usd = ["1000000", '5000000', '10000000']
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_fwd,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_1w}]
        self.sts_filled = Status.Fill
        self.sts_rejected = Status.Reject
        self.md_req_id = 'EUR/USD:SPO:REG:HSBC'

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.fix_md.set_market_data(). \
            update_value_in_repeating_group("NoMDEntries", "MDQuoteType", '0'). \
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_md.update_MDReqID(self.md_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD IND")
        self.sleep(10)
        # endregion

        # region Step 2
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)

        self.md_snapshot.set_params_for_md_response(self.md_request, self.bands_eur_usd, published=False)
        self.sleep(4)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot)
        # endregion

        # region Step 3
        self.new_order_single.set_default().change_parameters(
            {"Instrument": self.instrument,
             "SettlDate": self.settle_date_1w,
             "SettlType": self.settle_type_1w,
             "TimeInForce": "3"})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_rejected)
        self.execution_report.change_parameter("Text", "not tradeable")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

        # region Step 4
        self.new_order_single.set_default()
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report_doubler.set_params_from_new_order_single(self.new_order_single, self.sts_filled)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Step 5
        self.fix_md.set_market_data(). \
            update_MDReqID(self.fix_md.get_parameter("MDReqID"), self.fix_env.feed_handler, 'FX')
        self.fix_md.update_MDReqID(self.md_req_id, self.fix_env.feed_handler, "FX")
        self.fix_manager_fh.send_message(self.fix_md, "Send MD HSBC EUR/USD TRD")
        # endregion
