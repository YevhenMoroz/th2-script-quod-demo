import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4829(TestCase):
    @try_except(test_id=Path(__file__).name[:-3])
    def __init__(self, report_id, data_set=None, environment=None):
        super().__init__(report_id=report_id, data_set=data_set, environment=environment)
        self.test_id = bca.create_event(Path(__file__).name[:-3], self.report_id)

        self.fix_env1 = self.environment.get_list_fix_environment()[0]

        # region th2 components
        self.fix_manager_sell = FixManager(self.fix_env1.sell_side, self.test_id)
        self.fix_manager_feed_handler = FixManager(self.fix_env1.feed_handler, self.test_id)
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region order parameters
        self.qty = 100
        self.display_qty = 50
        self.price = 3.05
        self.stop_price = 3.056
        self.price_ask = 40
        self.price_bid = 1
        self.qty_bid = self.qty_ask = 1000000
        self.order_type_stop_lmt = constants.OrderType.StopLimit.value
        self.tif_gtc = constants.TimeInForce.GoodTillCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_multiple_n.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_13")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit6 = self.data_set.get_mic_by_name("mic_18")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl6 = self.data_set.get_listing_id_by_name("listing_11")
        self.listing_id_qdl7 = self.data_set.get_listing_id_by_name("listing_12")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl6 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl6, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl6.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl6)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl7 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl7, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl7.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl7.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl7)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SynthMinQty order
        case_id_1 = bca.create_event("Create SORPING STL GTC Iceberg Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_STL_GTC_Iceberg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multiple_Emulation_params()
        self.SORPING_STL_GTC_Iceberg_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_STL_GTC_Iceberg_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, TimeInForce=self.tif_gtc, ClientAlgoPolicyID=self.algopolicy, OrdType=self.order_type_stop_lmt)).add_tag(dict(StopPx=self.stop_price, DisplayInstruction=dict(DisplayQty=self.display_qty)))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_STL_GTC_Iceberg_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_STL_GTC_Iceberg_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_STL_GTC_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_STL_GTC_Iceberg_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_STL_GTC_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_STL_GTC_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_STL_GTC_Iceberg_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_STL_GTC_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Eliminate Algo order
        er_eliminate_SORPING_STL_GTC_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_STL_GTC_Iceberg_order, self.gateway_side_sell, self.status_eliminate)
        er_eliminate_SORPING_STL_GTC_Iceberg_order_params.add_tag(dict(Text='Multi-day validity synthesisation forbidden by algorithm parameters - child order blocked by internal validation'))
        self.fix_verifier_sell.check_fix_message(er_eliminate_SORPING_STL_GTC_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Eliminate')
        # endregion
