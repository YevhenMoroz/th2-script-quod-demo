import time
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum, Status
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageExecutionReportFX import FixMessageExecutionReportFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.fix_wrappers.forex.FixMessageNewOrderSingleFX import FixMessageNewOrderSingleFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T2749(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, session_id=None, data_set: BaseDataSet = None, environment: FullEnvironment = None):
        super().__init__(report_id, session_id, data_set, environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)
        self.fix_env = self.environment.get_list_fix_environment()[0]
        self.java_api_env = self.environment.get_list_java_api_environment()[0].java_api_conn
        self.java_manager = JavaApiManager(self.java_api_env, self.test_id)
        self.fix_manager_gtw = FixManager(self.fix_env.sell_side_esp, self.test_id)
        self.adjustment_request = QuoteAdjustmentRequestFX(data_set=self.data_set)
        self.fix_verifier = FixVerifier(self.fix_env.sell_side_esp, self.test_id)
        self.md_request = FixMessageMarketDataRequestFX(data_set=self.data_set)
        self.new_order_single = FixMessageNewOrderSingleFX(data_set=self.data_set)
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.execution_report = FixMessageExecutionReportFX()
        self.konstantin = self.data_set.get_client_by_name("client_mm_12")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.verifier = Verifier
        self.default_bid_px = None
        self.default_ask_px = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region 1-2
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.default_bid_px = response[0].get_parameter("NoMDEntries")[0]["MDEntryPx"]
        self.default_ask_px = response[0].get_parameter("NoMDEntries")[1]["MDEntryPx"]
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region 3-4
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.adjustment_request.update_margins_by_index(1, "0", "0.2")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(4)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = round(float(self.default_bid_px), 5)
        modified_ask_px = round(float(self.default_ask_px) + 0.00002, 5)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(4)
