import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.data_sets.constants import StrategyParameterType, OrderSide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import OrderType


class QAP_T4272(TestCase):
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
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1_000_000
        self.order_type = OrderType.Stop.value
        self.char_type = StrategyParameterType.Char.value
        self.float_type = StrategyParameterType.Float.value
        self.trigger_px_type = 'MarketBestBidOffer'
        self.offset_val = -5
        self.side = OrderSide.Sell.value
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_1")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_4")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.trailingstop_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_TrailingStop_params()
        self.trailingstop_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.trailingstop_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, Side=self.side))
        self.trailingstop_order.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='OffsetValue', StrategyParameterType=self.float_type, StrategyParameterValue=self.offset_val),
                                                                                dict(StrategyParameterName='TriggerPriceType', StrategyParameterType=self.char_type, StrategyParameterValue=self.trigger_px_type)])
        self.fix_manager_sell.send_message_and_receive_response(self.trailingstop_order, case_id_1)
        # endregion

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.trailingstop_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_trailingstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.trailingstop_order, self.gateway_side_sell, self.status_pending)
        pending_trailingstop_order_params.remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(pending_trailingstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_trailingstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.trailingstop_order, self.gateway_side_sell, self.status_new)
        new_trailingstop_order_params.remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(new_trailingstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_trailingstop_order = FixMessageOrderCancelRequest(self.trailingstop_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_trailingstop_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_trailingstop_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        cancel_trailingstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.trailingstop_order, self.gateway_side_sell, self.status_cancel)
        cancel_trailingstop_order_params.remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(cancel_trailingstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion
