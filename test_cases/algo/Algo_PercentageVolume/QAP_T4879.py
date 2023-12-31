import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.algo_formulas_manager import AlgoFormulasManager

class QAP_T4879(TestCase):
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
        self.order_type = constants.OrderType.Limit.value
        self.qty = 1000
        self.start_ltq = 200
        self.start_open_ord_qty = 100
        self.open_ord_qty = 500
        self.open_ord_dec_qty = 150
        self.pct = 0.3
        self.child_ltq_qty = AlgoFormulasManager.get_pov_child_qty(self.pct, self.start_ltq, self.qty) # 86
        self.child_md_qty = AlgoFormulasManager.get_pov_child_qty(self.pct, self.start_open_ord_qty, self.qty-self.child_ltq_qty) # 43
        self.child_md_qty_mod = AlgoFormulasManager.get_pov_child_qty(self.pct, self.open_ord_qty, self.qty-self.child_ltq_qty) # 215
        self.child2_md_qty = AlgoFormulasManager.get_pov_child_qty(self.pct, self.open_ord_dec_qty, self.qty-self.child_ltq_qty) # 65
        self.MDSize1 = self.start_open_ord_qty + self.child_ltq_qty # 186 -> MD child calculated as 30% of 100=43
        self.MDSize2 = self.open_ord_qty + self.child_ltq_qty + self.child_md_qty # 629 -> MD child 2 calculated as 30% of 500=215
        self.MDSize3 = self.open_ord_dec_qty + self.child_ltq_qty # 236 -> MD child 3 calculated as 30% of 150=65
        self.aggressivity_neut = constants.Aggressivity.Neutral.value
        self.price_ask = 1
        self.price = self.price_bid = 1
        self.qty_bid = self.qty_ask = 1_000_000
        self.tif_day = constants.TimeInForce.Day.value
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_cancel_replace = Status.CancelReplace
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
        rule_manager = RuleManager(Simulators.algo)
        nos_dma_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [ocr_rule, nos_dma_rule, ocrr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        #endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.POV_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_params()
        self.POV_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.POV_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.POV_order.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='PercentageVolume', StrategyParameterType=6, StrategyParameterValue=self.pct)])
        self.POV_order.add_fields_into_repeating_group('NoStrategyParameters', [{'StrategyParameterName': 'Aggressivity', 'StrategyParameterType': 1, 'StrategyParameterValue': self.aggressivity_neut}])
        self.fix_manager_sell.send_message_and_receive_response(self.POV_order, case_id_1)
        # endregion

        time.sleep(2)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.price_bid, MDEntrySize=self.start_ltq)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        time.sleep(2)

        # region Check child DMA order LTQ
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order LTQ", self.test_id))

        self.dma_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_1.change_parameters(dict(OrderQty=self.child_ltq_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day))
        self.fix_verifier_buy.check_fix_message(self.dma_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA order LTQ')

        self.pending_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order LTQ')

        self.new_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Aggressive Child DMA order LTQ')
        #endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data for Passive Child", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.MDSize1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        #endregion

        time.sleep(2)

        # region Check child DMA order MD 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive Child DMA order 1", self.test_id))

        self.dma_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params(False)
        self.dma_order_2.change_parameters(dict(OrderQty=self.child_md_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day))
        self.fix_verifier_buy.check_fix_message(self.dma_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child DMA order 1')

        self.pending_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child DMA order 1')

        self.new_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child DMA order 1')
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data - Increase Bid for Passive child qty modification", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.MDSize2)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        #endregion

        time.sleep(2)

        # region Check OCRR for Passive child
        self.replace_dma_params = FixMessageOrderCancelReplaceRequestAlgo(self.dma_order_2)
        self.replace_dma_params.change_parameters(dict(OrderQty=self.child_md_qty_mod))
        self.fix_verifier_buy.check_fix_message(self.replace_dma_params, key_parameters=self.key_params, message_name='Buy side OCRR Passive Child DMA order 1')

        er_replace_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_cancel_replace)
        er_replace_dma_1_order_params.change_parameters(dict(OrderQty=self.child_md_qty_mod))
        self.fix_verifier_buy.check_fix_message(er_replace_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Replaced Passive Child DMA order 1')
        # endregion

        # region Check cancel for Passive child
        self.cancel_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_cancel)
        self.cancel_dma_order_2_params.change_parameter('OrderQty', self.child_md_qty_mod)
        self.fix_verifier_buy.check_fix_message(self.cancel_dma_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA order MD 1')

        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data - Increase Bid for releasing Passive child 2", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.MDSize3)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Check Passive child DMA order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive child DMA order 2", self.test_id))

        self.dma_order_4 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_4.change_parameters(dict(OrderQty=self.child2_md_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day))
        self.fix_verifier_buy.check_fix_message(self.dma_order_4, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive child DMA order 2')

        self.pending_dma_order_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_4, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_4_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive child DMA order 2')

        self.new_dma_order_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_4, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_4_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Passive child DMA order 2')
        # endregion

        time.sleep(2)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        self.fix_verifier_buy.set_case_id(case_id_3)

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.POV_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        #endregion

        time.sleep(5)

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport Canceled')
        # endregion

        time.sleep(2)

        # region check cancellation child orders (DMA LTQ and Passive Child 2)
        self.cancel_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(self.cancel_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Child DMA order LTQ')

        self.cancel_dma_order_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_4, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(self.cancel_dma_order_4_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel Passive child DMA order 2')
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)
