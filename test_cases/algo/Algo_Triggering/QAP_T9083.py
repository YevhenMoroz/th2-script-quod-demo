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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T9083(TestCase):
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
        self.ord_type = constants.OrderType.Market.value
        self.qty = 1000
        self.price_ask_agta = 24
        self.price_bid_agta = 23
        self.price_ask_par = 23
        self.price_ask_par_2 = 24
        self.price_bid_par = 21
        self.qty_bid = 100
        self.qty_ask = 500
        # endregion

        # region Gateway Side
        self.gateway_side_sell = GatewaySide.Sell
        self.gateway_side_buy = GatewaySide.Buy
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_partialfill = Status.PartialFill
        self.status_eliminate = Status.Eliminate
        self.status_cancel_replace = Status.CancelReplace
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
        # endregion

        # region Trigger params init
        self.trigger_instrument = self.data_set.get_fix_instrument_by_name("instrument_39")
        self.trigger_type = constants.TriggerType.PriceMovement.value
        self.trig_px_direct = constants.TriggerPriceDirection.PriceGoesDown.value
        self.trigger_px = 22
        self.trig_px_type = constants.TriggerPriceType.BestBidOrLastTrade.value
        self.trig_symbol = self.trigger_instrument['Symbol']
        self.trig_security_id = self.trigger_instrument['SecurityID']
        self.trig_security_id_source = self.trigger_instrument['SecurityIDSource']
        # endregion

        # region Trigger params mod
        self.trig_symbol_mod = self.instrument['Symbol']
        self.trig_security_id_mod = self.instrument['SecurityID']
        self.trig_security_id_source_mod = self.instrument['SecurityIDSource']
        self.trig_px_direct_mod = constants.TriggerPriceDirection.PriceGoesUp.value
        self.trigger_px_mod = 24
        self.trig_px_type_mod = constants.TriggerPriceType.BestOffer.value
        self.s_agta = self.data_set.get_listing_id_by_name("listing_59")
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
        nos_mkt_rule = rule_manager.add_NewOrdSingle_Market(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.qty_ask, self.price_ask_par_2)

        self.rule_list = [nos_mkt_rule]
        # endregion
        
        # region Send_MarkerData PAR
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data PAR", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_par, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_par, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion
        
        # region Send_MarkerData AGTA
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data AGTA", self.test_id))
        market_data_snap_shot_agta = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_agta, self.fix_env1.feed_handler)
        market_data_snap_shot_agta.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_agta, MDEntrySize=self.qty_bid)
        market_data_snap_shot_agta.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_agta, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_agta)
        # endregion

        # region Send NewOrderSingle (35=D) for Triggering order
        case_id_1 = bca.create_event("Create Triggering Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Triggering_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Triggering_params()
        self.Triggering_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Triggering_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, OrdType=self.ord_type)).remove_parameter('Price')
        self.Triggering_order.update_fields_in_component('TriggeringInstruction', dict(TriggerSymbol=self.trig_symbol, TriggerSecurityID=self.trig_security_id, TriggerSecurityIDSource=self.trig_security_id_source,
                                                                                        TriggerPriceType=self.trig_px_type, TriggerPriceDirection=self.trig_px_direct, TriggerPrice=self.trigger_px))
        self.fix_manager_sell.send_message_and_receive_response(self.Triggering_order, case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Triggering_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_new)
        
        self.fix_verifier_sell.check_fix_message(new_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(2)
        
        # region Send OCRR (35=G) for Triggering order
        case_id_2 = bca.create_event("Modify Triggering Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.Triggering_order_modify = FixMessageOrderCancelReplaceRequestAlgo(self.Triggering_order)
        self.Triggering_order_modify.update_fields_in_component('TriggeringInstruction', dict(TriggerSymbol=self.trig_symbol_mod, TriggerSecurityID=self.trig_security_id_mod, TriggerSecurityIDSource=self.trig_security_id_source_mod,
                                                                                        TriggerPriceType=self.trig_px_type_mod, TriggerPriceDirection=self.trig_px_direct_mod, TriggerPrice=self.trigger_px_mod))

        self.fix_manager_sell.send_message_and_receive_response(self.Triggering_order_modify, case_id_2)
        # endregion

        time.sleep(2)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Triggering_order_modify, key_parameters=self.key_params, direction=self.ToQuod, message_name='Sell side OCRR')

        replaced_Triggering_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(replaced_Triggering_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Replaced')
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data PAR", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_par, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_par_2, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order.change_parameters(dict(OrderQty=self.qty, OrdType=self.ord_type, Instrument='*')).remove_parameter('Price')
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA')

        self.pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA')

        self.new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA')

        self.fill_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_partialfill)
        self.fill_dma_order_params.change_parameter('Price', '*')
        self.fix_verifier_buy.check_fix_message(self.fill_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Partial Fill Child DMA')
        # endregion

        # region check fill Parent SS
        part_fill_Triggering_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Triggering_order, self.gateway_side_sell, self.status_partialfill)
        self.fix_verifier_sell.check_fix_message(part_fill_Triggering_order, message_name='Sell side ExecReport Partial Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager(Simulators.algo).remove_rules(self.rule_list)
