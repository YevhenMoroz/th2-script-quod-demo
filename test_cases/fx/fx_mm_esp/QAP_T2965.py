from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.win_gui_wrappers.fe_trading_constant import PricingButtonColor
from test_framework.win_gui_wrappers.forex.client_rates_tile import ClientRatesTile
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
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T2965(TestCase):
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.rates_tile = ClientRatesTile(self.test_id, self.session_id)
        self.client = self.data_set.get_client_tier_by_name("client_tier_1")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.instrument = self.eur_usd + "-Spot"
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.execution_report_2 = FixMessageExecutionReportFX()
        self.sliver = self.data_set.get_client_by_name("client_mm_1")
        self.security_type_spot = self.data_set.get_security_type_by_name('fx_spot')
        self.settle_type_spot = self.data_set.get_settle_type_by_name('spot')
        self.bands_eur_usd = ["*", '*', '*']
        self.qty_5m = "5000000"
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type_spot,
            'Product': '4', }
        self.no_related_symbols = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_spot}]
        self.sts_filled = Status.Fill
        self.sts_reject = Status.Reject

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Step 1
        self.rates_tile.crete_tile()
        self.rates_tile.modify_client_tile(instrument=self.eur_usd, client_tier=self.client)

        self.rates_tile.press_pricing()

        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.new_order_single.set_default()
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_reject)
        self.execution_report.change_parameter("Text", "not active")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)

        self.rates_tile.press_pricing()
        self.rates_tile.select_rows([2, 3])
        self.rates_tile.press_pricing()

        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.new_order_single.set_default()
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report_2.set_params_from_new_order_single(self.new_order_single, self.sts_filled)
        self.fix_verifier.check_fix_message(fix_message=self.execution_report_2, direction=DirectionEnum.FromQuod)

        self.md_request.set_md_req_parameters_maker()
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.new_order_single.set_default().change_parameters({"OrderQty": self.qty_5m})
        self.fix_manager_gtw.send_message_and_receive_response(self.new_order_single, self.test_id)
        self.execution_report.set_params_from_new_order_single(self.new_order_single, self.sts_reject)
        self.execution_report.change_parameter("Text", "not enough quantity in book")
        self.fix_verifier.check_fix_message(fix_message=self.execution_report, direction=DirectionEnum.FromQuod)

        self.rates_tile.press_pricing()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.rates_tile.close_tile()
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
