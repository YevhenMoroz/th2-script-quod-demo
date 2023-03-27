import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T9031(TestCase):
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
        self.price = 22
        self.qty = 1000
        self.side = constants.OrderSide.Sell.value
        self.price_ask = 24
        self.price_bid = 21
        self.price_bid_2 = 22
        self.qty_bid_1 = self.qty_ask = 100
        self.qty_bid_2 = 200
        self.strat_param_type_int = constants.StrategyParameterType.Float.value
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Trigger params
        self.trigger_instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        self.trigger_type = constants.TriggerType.PriceMovement.value
        self.trig_px_direct = constants.TriggerPriceDirection.PriceGoesUp.value
        self.trigger_px = 22
        self.trig_px_type = constants.TriggerPriceType.BestBidOrLastTrade.value
        self.trig_symbol = self.trigger_instrument['Symbol']
        self.trig_security_id = self.trigger_instrument['SecurityID']
        self.trig_security_id_source = self.trigger_instrument['SecurityIDSource']
        self.min_trig_qty = 200

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
        trade_dma_rule = rule_manager.add_NewOrdSingleExecutionReportTrade(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price, self.qty, 2000)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)

        self.rule_list = [ocr_rule, nos_dma_rule, trade_dma_rule]
        # endregion
        
        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid_1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Send NewOrderSingle (35=D) for Triggering order
        case_id_1 = bca.create_event("Create Triggering Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.Triggering_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Triggering_params()
        self.Triggering_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Triggering_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, Side=self.side))
        self.Triggering_order.update_fields_in_component('TriggeringInstruction', dict(TriggerSymbol=self.trig_symbol, TriggerSecurityID=self.trig_security_id, TriggerSecurityIDSource=self.trig_security_id_source,
                                                                                        TriggerPriceType=self.trig_px_type, TriggerPriceDirection=self.trig_px_direct, TriggerPrice=self.trigger_px))
        self.Triggering_order.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='MinTriggerQty', StrategyParameterType=self.strat_param_type_int, StrategyParameterValue=self.min_trig_qty)])
        self.fix_manager_sell.send_message_and_receive_response(self.Triggering_order, case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Triggering_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_2, MDEntrySize=self.qty_bid_1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_2, MDEntrySize=self.qty_bid_2)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Check child DMA order
        self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order.change_parameters(dict(OrderQty=self.qty, Price=self.price, Instrument='*', Side=self.side, MinQty=self.min_trig_qty))
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA')

        self.pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA')

        self.new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA')

        self.fill_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(self.fill_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA')
        
        self.fix_verifier_buy.check_fix_message_sequence([self.pending_dma_order_params, self.new_dma_order_params, self.fill_dma_order_params],
                                                         [None, None, None], self.ToQuod, "Check sequence only one child order is created")
        # endregion

        # region check fill Parent order
        fill_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(fill_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        RuleManager(Simulators.algo).remove_rules(self.rule_list)
