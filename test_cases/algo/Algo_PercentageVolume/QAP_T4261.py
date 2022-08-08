import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4261(TestCase):
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
        self.qty = 300
        self.child_qty = 13
        self.price = 1
        self.childMinValue = 150
        self.volume = 0.5
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.md_entry_px_incr_r = 1
        self.md_entry_size_incr_r = 360 # for partially fill
        self.md_entry_size_incr_r_new = 300 # child is created
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1000000
        self.md_entry_px_incr_r_reset = self.md_entry_size_incr_r_reset = 0
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
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
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager()
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, 180, self.price)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_ioc_rule, nos_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.POV_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_min_value_params()
        self.POV_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.POV_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument)) # NoStrategyParameters=[dict(dict(PercentageVolume=self.volume))]))

        self.fix_manager_sell.send_message_and_receive_response(self.POV_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)  # 1015
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r, MDEntrySize=self.md_entry_size_incr_r)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion
        
        time.sleep(3)

        # region Update LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)  # 1015
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r, MDEntrySize=self.md_entry_size_incr_r_new)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(3)
        # endregion

        # region Reset LTQ
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)  # 1015
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.md_entry_px_incr_r_reset, MDEntrySize=self.md_entry_size_incr_r_reset)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        time.sleep(3)
        # endregion
    #
    #     # region Check child DMA order
    #     self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA 1 order", self.test_id))
    #
    #     self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
    #     self.dma_order.change_parameters(dict(OrderQty=self.child_qty, Price=self.price, Instrument=self.instrument))
    #     self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 1 order')
    #
    #     pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
    #     self.fix_verifier_buy.check_fix_message(pending_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')
    #
    #     new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
    #     self.fix_verifier_buy.check_fix_message(new_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
    #     # endregion
    #
    # @try_except(test_id=Path(__file__).name[:-3])
    # def run_post_conditions(self):
    #     # region Cancel Algo Order
    #     case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
    #     self.fix_verifier_sell.set_case_id(case_id_3)
    #     cancel_request_POV_order = FixMessageOrderCancelRequest(self.POV_order)
    #
    #     self.fix_manager_sell.send_message_and_receive_response(cancel_request_POV_order, case_id_3)
    #     self.fix_verifier_sell.check_fix_message(cancel_request_POV_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
    #
    #     # region check cancel second dma child order
    #     cancel_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
    #     self.fix_verifier_buy.check_fix_message(cancel_dma_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel child DMA 2 order")
    #     # endregion
    #
    #     cancel_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_cancel)
    #     self.fix_verifier_sell.check_fix_message(cancel_POV_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
    #     # endregion
        
        rule_manager = RuleManager()
        rule_manager.remove_rules(self.rule_list)
