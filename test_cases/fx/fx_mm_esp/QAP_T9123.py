from pathlib import Path
from decimal import *
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import Status
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX


class QAP_T9123(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.dealer_intervention = None
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.silver = self.data_set.get_client_by_name("client_mm_1")
        self.eur_usd = self.data_set.get_symbol_by_name('symbol_1')
        self.security_type = self.data_set.get_security_type_by_name("fx_fwd")
        self.settle_type_2w = self.data_set.get_settle_type_by_name("wk2")
        self.settle_type_3w = self.data_set.get_settle_type_by_name("wk3")
        self.settle_type_1m = self.data_set.get_settle_type_by_name("m1")
        self.status_reject = Status.Reject
        self.instrument = {
            'Symbol': self.eur_usd,
            'SecurityType': self.security_type,
            'Product': '4', }
        self.no_related_symbols_2w = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_2w}]
        self.no_related_symbols_3w = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_3w}]
        self.no_related_symbols_1m = [{
            'Instrument': self.instrument,
            'SettlType': self.settle_type_1m}]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Examionation
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_2w)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        fwd_points_bid_2w = response[0].get_parameter("NoMDEntries")[0]['MDEntryForwardPoints']
        fwd_points_ask_2w = response[0].get_parameter("NoMDEntries")[1]['MDEntryForwardPoints']

        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_1m)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        fwd_points_bid_1m = response[0].get_parameter("NoMDEntries")[0]['MDEntryForwardPoints']
        fwd_points_ask_1m = response[0].get_parameter("NoMDEntries")[1]['MDEntryForwardPoints']
        # endregion
        # region step 1
        self.md_request.set_md_req_parameters_maker()
        self.md_request.update_repeating_group('NoRelatedSymbols', self.no_related_symbols_3w)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        fwd_points_bid = (Decimal(fwd_points_bid_2w) + (Decimal(23) - Decimal(16)) / (Decimal(33) - Decimal(16)) * (
                    Decimal(fwd_points_bid_1m) - Decimal(fwd_points_bid_2w)))
        fwd_points_ask = (Decimal(fwd_points_ask_2w) + (Decimal(23) - Decimal(16)) / (Decimal(33) - Decimal(16)) * (
                    Decimal(fwd_points_ask_1m) - Decimal(fwd_points_ask_2w)))

        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryForwardPoints=f"{fwd_points_bid:.5f}",
                                                         SettlDate="*", MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryForwardPoints=f"{fwd_points_ask:.5f}",
                                                         SettlDate="*", MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryForwardPoints=f"{fwd_points_bid:.5f}",
                                                         SettlDate="*",
                                                         MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryForwardPoints=f"{fwd_points_ask:.5f}",
                                                         SettlDate="*", MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryForwardPoints=f"{fwd_points_bid:.5f}",
                                                         SettlDate="*", MDEntrySpotRate="*")
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryForwardPoints=f"{fwd_points_ask:.5f}",
                                                         SettlDate="*", MDEntrySpotRate="*")
        self.fix_verifier.check_fix_message(self.md_snapshot, ignored_fields=["trailer", "header", "CachedUpdate"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
