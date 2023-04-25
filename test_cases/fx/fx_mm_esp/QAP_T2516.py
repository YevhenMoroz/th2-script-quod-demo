from pathlib import Path
from custom import basic_custom_actions as bca
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.environments.full_environment import FullEnvironment
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.fix_wrappers.forex.FixMessageMarketDataRequestFX import FixMessageMarketDataRequestFX
from test_framework.fix_wrappers.forex.FixMessageMarketDataSnapshotFullRefreshSellFX import \
    FixMessageMarketDataSnapshotFullRefreshSellFX
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T2516(TestCase):
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
        self.md_snapshot = FixMessageMarketDataSnapshotFullRefreshSellFX()
        self.konstantin = self.data_set.get_client_by_name("client_mm_12")
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.default_bid_px_1 = None
        self.default_ask_px_1 = None
        self.default_bid_px_2 = None
        self.default_ask_px_2 = None
        self.default_bid_px_3 = None
        self.default_ask_px_3 = None

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region 1-2
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.adjustment_request.update_margins_by_index(1, "0", "0")
        self.adjustment_request.update_margins_by_index(2, "0", "0")
        self.adjustment_request.update_margins_by_index(3, "0", "0")
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(2)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.default_bid_px_1 = response[0].get_parameter("NoMDEntries")[0]["MDEntryPx"]
        self.default_ask_px_1 = response[0].get_parameter("NoMDEntries")[1]["MDEntryPx"]
        self.default_bid_px_2 = response[0].get_parameter("NoMDEntries")[2]["MDEntryPx"]
        self.default_ask_px_2 = response[0].get_parameter("NoMDEntries")[3]["MDEntryPx"]
        self.default_bid_px_3 = response[0].get_parameter("NoMDEntries")[4]["MDEntryPx"]
        self.default_ask_px_3 = response[0].get_parameter("NoMDEntries")[5]["MDEntryPx"]
        # endregion

        # region 3-4
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.adjustment_request.update_margins_by_index(1, "-0.1", "0.1")
        self.adjustment_request.update_margins_by_index(2, "-0.2", "0.2")
        self.adjustment_request.update_margins_by_index(3, "-0.3", "0.3")
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px_1 = round(float(self.default_bid_px_1) + 0.00001, 6)
        modified_ask_px_1 = round(float(self.default_ask_px_1) + 0.00001, 6)
        modified_bid_px_2 = round(float(self.default_bid_px_2) + 0.00002, 6)
        modified_ask_px_2 = round(float(self.default_ask_px_2) + 0.00002, 6)
        modified_bid_px_3 = round(float(self.default_bid_px_3) + 0.00003, 6)
        modified_ask_px_3 = round(float(self.default_ask_px_3) + 0.00003, 6)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=modified_bid_px_1)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=modified_ask_px_1)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px_2)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px_2)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryPx=modified_bid_px_3)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryPx=modified_ask_px_3)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

        # region 4
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.adjustment_request.update_margins_by_index(1, "0", "0")
        self.adjustment_request.update_margins_by_index(2, "0", "0")
        self.adjustment_request.update_margins_by_index(3, "0", "0")
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 0, MDEntryPx=self.default_bid_px_1)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 1, MDEntryPx=self.default_ask_px_1)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=self.default_bid_px_2)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=self.default_ask_px_2)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 4, MDEntryPx=self.default_bid_px_3)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 5, MDEntryPx=self.default_ask_px_3)
        self.fix_verifier.check_fix_message(self.md_snapshot)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument(self.eur_usd)
        self.java_manager.send_message(self.adjustment_request)
        self.sleep(2)
