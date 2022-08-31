import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_T4070(TestCase):
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
        self.qty = 350
        self.min_qty = 200
        self.inc_min_qty = 300
        self.price = 15
        self.price_ask = 40
        self.price_bid_qdl1 = 11
        self.price_bid_qdl2 = 10
        self.qty_bid = 200
        self.qty_ask = 1000000
        self.px_for_incr = 0
        self.qty_for_incr = 0
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_8")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_ER_cancel_reject_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_parent")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        now = datetime.today() - timedelta(hours=3)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl1, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        market_data_snap_shot_qdl1 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl2, MDEntrySize=self.qty_bid)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        market_data_snap_shot_qdl2 = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for Synth MinQty_order order
        case_id_1 = bca.create_event("Create Synth MinQty Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.synthMinQty_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SynthMinQty_params()
        self.synthMinQty_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.synthMinQty_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, MinQty=self.min_qty))

        self.fix_manager_sell.send_message_and_receive_response(self.synthMinQty_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.synthMinQty_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_synthMinQty_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_synthMinQty_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_synthMinQty_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_synthMinQty_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Modify parent MP Dark order
        case_id_2 = bca.create_event("Replace Synth MinQty Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.synthMinQty_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.synthMinQty_order)
        self.synthMinQty_order_replace_params.change_parameters(dict(MinQty=self.inc_min_qty))
        self.fix_manager_sell.send_message_and_receive_response(self.synthMinQty_order_replace_params, case_id_2)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.synthMinQty_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_reject_replaced_synthMinQty_order_params = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_new)
        er_reject_replaced_synthMinQty_order_params.change_parameters(dict(CxlRejResponseTo='2'))
        self.fix_verifier_sell.check_fix_message(er_reject_replaced_synthMinQty_order_params, key_parameters=self.key_params_ER_cancel_reject_parent, message_name='Sell Side OrderCancelRejectReport')
        # endregion

        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_synthMinQty_order = FixMessageOrderCancelRequest(self.synthMinQty_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_synthMinQty_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_synthMinQty_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        er_cancel_synthMinQty_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthMinQty_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_synthMinQty_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion