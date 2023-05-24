import os
import time
from pathlib import Path
from datetime import datetime, timedelta

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

class QAP_T4890(TestCase):
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
        self.pct = 0.3
        self.aggressivity_neut = constants.Aggressivity.Neutral.value
        self.aggressivity_aggr = constants.Aggressivity.Aggressive.value
        self.price_ask = 1
        self.price = self.price_bid = 1
        self.qty_bid = self.qty_ask = 1_000_000
        self.start_ltq = 200
        self.open_ord_qty = 60
        self.ioc_qty = 40
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.tif_day = constants.TimeInForce.Day.value
        self.child_ltq_qty = AlgoFormulasManager.get_pov_child_qty(self.pct, self.open_ord_qty, self.qty)
        self.child_md_qty = AlgoFormulasManager.get_pov_child_qty(self.pct, self.open_ord_qty, self.qty-self.child_ltq_qty)
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_fill = Status.Fill
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_cancel_replace = Status.CancelReplace
        self.status_eliminate = Status.Eliminate
        self.status_partfill = Status.PartialFill
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
        nos_trade = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_1, 1, 1, self.child_ltq_qty, self.child_ltq_qty, 3)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, 0, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)

        self.rule_list = [ocr_rule, nos_dma_rule, nos_ioc_rule, nos_trade]
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.price_bid, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.open_ord_qty)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

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

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.price_bid, MDEntrySize=self.open_ord_qty)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=0, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.open_ord_qty)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.POV_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_POV_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_POV_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(5)

        # region Check child DMA order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))
        
        self.dma_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_1.change_parameters(dict(OrderQty=self.child_ltq_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_day))
        self.fix_verifier_buy.check_fix_message(self.dma_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Slice 1')

        self.pending_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Slice 1')

        self.new_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Slice 1')

        time.sleep(5)

        # region Modify parent POV order
        case_id_2 = bca.create_event("Replace POV Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        self.fix_verifier_buy.set_case_id(case_id_2)

        self.POV_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.POV_order)
        self.POV_order_replace_params.update_repeating_group('NoStrategyParameters', [{'StrategyParameterName': 'Aggressivity', 'StrategyParameterType': 1, 'StrategyParameterValue': self.aggressivity_aggr},
                                                                                      {'StrategyParameterName': 'PercentageVolume', 'StrategyParameterType': 6, 'StrategyParameterValue': self.pct}])
        self.fix_manager_sell.send_message_and_receive_response(self.POV_order_replace_params, case_id_2)

        time.sleep(1)

        self.POV_order_replace_params.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(self.POV_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        replaced_twap_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.POV_order_replace_params, self.gateway_side_sell, self.status_partfill)
        self.fix_verifier_sell.check_fix_message(replaced_twap_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region Check child DMA order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order 2", self.test_id))
        self.dma_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_2.change_parameters(dict(OrderQty=self.child_md_qty, Price=self.price, Instrument='*', TimeInForce=self.tif_ioc))

        self.fix_verifier_buy.check_fix_message(self.dma_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 2')

        pending_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2')

        new_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2')
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.price_bid, MDEntrySize=self.open_ord_qty)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().change_parameter('MDReqID', '1015_161')
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=0, MDEntrySize=0)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.open_ord_qty)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(5)

        # region check fill child DMA 1
        self.cancel_dma_order_1 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(self.cancel_dma_order_1, self.key_params, self.ToQuod, "Buy Side ExecReport Fill Child DMA 1")
        # endregion

        # region check eliminate child DMA 2
        cancel_dma_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message(cancel_dma_order_2, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate Child DMA 2")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        self.fix_verifier_buy.set_case_id(case_id_3)

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.POV_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(5)

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.POV_order, self.gateway_side_sell, self.status_cancel)
        cancel_pov_order.change_parameter('SettlType', '*')
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport Canceled')
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)
