import time
from datetime import datetime
from pathlib import Path
from custom import basic_custom_actions as bca
from custom.verifier import Verifier
from test_framework.core.test_case import TestCase
from test_framework.core.try_exept_decorator import try_except
from test_framework.data_sets.base_data_set import BaseDataSet
from test_framework.data_sets.constants import DirectionEnum
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
from test_framework.java_api_wrappers.JavaApiManager import JavaApiManager
from test_framework.java_api_wrappers.fx.QuoteAdjustmentRequestFX import QuoteAdjustmentRequestFX


class QAP_T2902(TestCase):
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
        self.fx_fh_connectivity = self.fix_env.feed_handler
        self.fix_md = FixMessageMarketDataSnapshotFullRefreshBuyFX()
        self.fix_manager_fh_314 = FixManager(self.fx_fh_connectivity, self.test_id)
        self.execution_report = FixMessageExecutionReportFX()
        self.konstantin = self.data_set.get_client_by_name("client_mm_12")
        self.verifier = Verifier
        self.default_bid_px = None
        self.default_ask_px = None
        self.eur_usd = self.data_set.get_symbol_by_name("symbol_1")
        self.hsbc = self.data_set.get_venue_by_name("venue_2")
        self.md_req_id = f"{self.eur_usd}:SPO:REG:{self.hsbc}"
        self.settle_date_spot = self.data_set.get_settle_date_by_name("spot")
        self.no_md_entries = [
            {"MDEntryType": "0",
             "MDEntryPx": 1.18,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.182,
             "MDEntrySize": 1000000,
             "MDEntryPositionNo": 1,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.175,
             "MDEntrySize": 3000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.19,
             "MDEntrySize": 3000000,
             "MDEntryPositionNo": 2,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "0",
             "MDEntryPx": 1.17,
             "MDEntrySize": 5000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')},
            {"MDEntryType": "1",
             "MDEntryPx": 1.195,
             "MDEntrySize": 5000000,
             "MDEntryPositionNo": 3,
             'SettlDate': self.settle_date_spot,
             "MDEntryTime": datetime.utcnow().strftime('%Y%m%d')}
        ]

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region 1-2
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_repeating_group("NoMDEntries", self.no_md_entries)
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        response: list = self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        default_bid_px_1 = response[0].get_parameter("NoMDEntries")[0]["MDEntryPx"]
        default_ask_px_1 = response[0].get_parameter("NoMDEntries")[1]["MDEntryPx"]
        default_bid_px_2 = response[0].get_parameter("NoMDEntries")[2]["MDEntryPx"]
        default_ask_px_2 = response[0].get_parameter("NoMDEntries")[3]["MDEntryPx"]
        default_bid_px_3 = response[0].get_parameter("NoMDEntries")[4]["MDEntryPx"]
        default_ask_px_3 = response[0].get_parameter("NoMDEntries")[5]["MDEntryPx"]
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"], response=response[0])
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region 3-4
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument("EUR/USD")
        self.adjustment_request.update_margins_by_index(2, "-2", "2")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0002
        modified_ask_px = float(default_ask_px_2) + 0.0002
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region 6
        self.adjustment_request.update_margins_by_index(2, "-1", "1")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0001
        modified_ask_px = float(default_ask_px_2) + 0.0001
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

        # region 7
        self.adjustment_request.update_margins_by_index(2, "-1", "3")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0001
        modified_ask_px = float(default_ask_px_2) + 0.0003
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        # region 7
        self.adjustment_request.update_margins_by_index(2, "-4", "3")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0004
        modified_ask_px = float(default_ask_px_2) + 0.0003
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        # region 7
        self.adjustment_request.update_margins_by_index(2, "-8", "-1")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0008
        modified_ask_px = float(default_ask_px_2) - 0.0001
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion
        # region 7
        self.adjustment_request.update_margins_by_index(2, "-3", "4")
        self.java_manager.send_message(self.adjustment_request)
        time.sleep(2)
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        modified_bid_px = float(default_bid_px_2) + 0.0003
        modified_ask_px = float(default_ask_px_2) + 0.0004
        self.md_snapshot.set_params_for_md_response(self.md_request, ["*", "*", "*"])
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 2, MDEntryPx=modified_bid_px)
        self.md_snapshot.update_repeating_group_by_index("NoMDEntries", 3, MDEntryPx=modified_ask_px)
        self.fix_verifier.check_fix_message(fix_message=self.md_snapshot,
                                            direction=DirectionEnum.FromQuod,
                                            key_parameters=["MDReqID"])
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        self.md_request.set_md_uns_parameters_maker()
        self.fix_manager_gtw.send_message(self.md_request)
        self.adjustment_request.set_defaults()
        self.adjustment_request.update_instrument("EUR/USD")
        self.java_manager.send_message(self.adjustment_request)

        self.md_request.set_md_req_parameters_maker().change_parameter("SenderSubID", self.konstantin)
        self.fix_manager_gtw.send_message_and_receive_response(self.md_request, self.test_id)
        self.fix_md.set_market_data()
        self.fix_md.update_MDReqID(self.md_req_id, self.fx_fh_connectivity, "FX")
        self.fix_manager_fh_314.send_message(self.fix_md)
        self.sleep(2)
