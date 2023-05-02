import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageNewOrderMultiLegAlgo import FixMessageNewOrderMultiLegAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T8584(TestCase):
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
        self.order_type = constants.OrderType.Market.value
        self.qty = 1000
        self.ratio_leg1 = 1.5
        self.ratio_leg2 = 2.5
        self.price_ask_init = 27
        self.price_ask_mod = 21
        self.price_bid = 20
        self.qty_bid = self.qty_ask = 1_000
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.spread_devi_type = "Currency"
        self.string_type = StrategyParameterType.String.value
        self.spread_devi_val = "5"
        self.float_type = StrategyParameterType.Float.value
        self.child1_qty_leg1 = int(self.qty * self.ratio_leg1)
        self.child2_qty_leg2 = int(self.qty * self.ratio_leg2)
        self.side_sell = constants.OrderSide.Sell.value
        self.side_buy = constants.OrderSide.Buy.value
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_fill = Status.Fill
        self.status_partfill = Status.PartialFill
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_cancel_replace = Status.CancelReplace
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_pt_float")
        self.instrumentleg_dp = self.data_set.get_fix_leg_instrument_by_name("instrument_dp")
        self.instrumentleg_sqi = self.data_set.get_fix_leg_instrument_by_name("instrument_sqi")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_par = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_par = self.data_set.get_account_by_name("account_2")
        self.leg_1 = self.data_set.get_listing_id_by_name("listing_dp")
        self.leg_2 = self.data_set.get_listing_id_by_name("listing_sqi")
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
        ioc_dma_rule_1 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, True, self.child1_qty_leg1, self.price_ask_mod)
        ioc_dma_rule_2 = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, True, self.child2_qty_leg2, self.price_bid)

        self.rule_list = [ioc_dma_rule_1, ioc_dma_rule_2]
        # endregion
        
        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Leg 1 DP", self.test_id))
        market_data_snap_shot_leg_1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.leg_1, self.fix_env1.feed_handler)
        market_data_snap_shot_leg_1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_leg_1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_init, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_leg_1)
        
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Leg 2 SQI", self.test_id))
        market_data_snap_shot_leg_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.leg_2, self.fix_env1.feed_handler)
        market_data_snap_shot_leg_2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_leg_2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_init, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_leg_2)
        # endregion

        time.sleep(2)

        # region Send NewOrderSingle (35=D) for PairTrad order
        case_id_1 = bca.create_event("Create PairTrad Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.PairTrad_order = FixMessageNewOrderMultiLegAlgo(data_set=self.data_set).set_PairTrading_params()
        self.PairTrad_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.PairTrad_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, OrdType=self.order_type, Instrument=self.instrument))
        self.PairTrad_order.update_repeating_group('NoLegs', [dict(InstrumentLeg=self.instrumentleg_dp), dict(LegRatioQty=self.ratio_leg1, LegSide=self.side_buy),
                                                              dict(InstrumentLeg=self.instrumentleg_sqi), dict(LegRatioQty=self.ratio_leg2, LegSide=self.side_sell)])
        self.PairTrad_order.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='SpreadDeviationNumber', StrategyParameterType=self.float_type, StrategyParameterValue=self.spread_devi_val),
                                                                            dict(StrategyParameterName='SpreadDeviationType', StrategyParameterType=self.string_type, StrategyParameterValue=self.spread_devi_type)])
        self.fix_manager_sell.send_message_and_receive_response(self.PairTrad_order, case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.PairTrad_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_PairTrad_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.PairTrad_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_PairTrad_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_PairTrad_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.PairTrad_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_PairTrad_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Leg 2 SQI", self.test_id))
        market_data_snap_shot_leg_2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.leg_1, self.fix_env1.feed_handler)
        market_data_snap_shot_leg_2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_leg_2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_mod, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_leg_2)
        # endregion

        time.sleep(5)

        # region Check child DMA order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order Leg 1", self.test_id))
        
        self.dma_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_1.change_parameters(dict(OrderQty=self.child1_qty_leg1, Price=self.price_ask_mod, Instrument='*', TimeInForce=self.tif_ioc, PositionEffect='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Leg 1')

        self.pending_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_pending)
        self.new_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_new)     
        self.fill_dma_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_1, self.gateway_side_buy, self.status_fill)
        # endregion

        # region Check child DMA order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order Leg 2", self.test_id))
        self.dma_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order_2.change_parameters(dict(OrderQty=self.child2_qty_leg2, Price=self.price_bid, Instrument='*', TimeInForce=self.tif_ioc, PositionEffect='*', Side=self.side_sell, LocateReqd='*'))

        self.fix_verifier_buy.check_fix_message(self.dma_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Leg 2')

        self.pending_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.new_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_new)
        self.fill_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_fill)
        # endregion

        # region Check sequence ER for child orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Check sequence ER for child orders", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.pending_dma_order_1_params, self.new_dma_order_1_params, self.fill_dma_order_1_params,
                                                          self.pending_dma_order_2_params, self.new_dma_order_2_params, self.fill_dma_order_2_params],
                                                         [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params],
                                                         self.ToQuod, "Check sequence ER for child orders", None, False)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):        
        # region check fill parent PairTrad order
        fill_PairTrad_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.PairTrad_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(fill_PairTrad_order, key_parameters=self.key_params_cl,  message_name='Sell side ExecReport filled')
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)
        