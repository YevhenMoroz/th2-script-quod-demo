import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_T4059(TestCase):
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
        self.qty = 1000
        self.mod_qty = 2000
        self.price = 20
        self.mod_price = 25
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1_000_000
        self.post_mode = 'Spraying'
        self.venue_weight_par = 'PARIS=7'
        self.venue_weight_trqx = 'TRQX=3'
        self.sum_weight = int(self.venue_weight_par[-1]) + int(self.venue_weight_trqx[-1])
        self.child_qty_par = int(self.qty * int(self.venue_weight_par[-1]) / self.sum_weight)
        self.child_qty_trqx = int(self.qty * int(self.venue_weight_trqx[-1]) / self.sum_weight)
        self.mod_child_qty_par = int(self.mod_qty * int(self.venue_weight_par[-1]) / self.sum_weight)
        self.mod_child_qty_trqx = int(self.mod_qty * int(self.venue_weight_trqx[-1]) / self.sum_weight)
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_5")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_par = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_par = self.data_set.get_account_by_name("account_2")
        self.account_trqx = self.data_set.get_account_by_name("account_5")
        self.listing_par = self.data_set.get_listing_id_by_name("listing_2")
        self.listing_trqx = self.data_set.get_listing_id_by_name("listing_3")
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
        nos_rule_par = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, self.price)
        nos_rule_par_mod = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, self.mod_price)
        ocr_rule_par = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, True)
        ocrr_rule_par = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account_par, self.ex_destination_par, True)

        nos_rule_trqx = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price)
        nos_rule_trqx_mod = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.mod_price)
        ocr_rule_trqx = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, True)
        ocrr_rule_trqx = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, True)

        self.rule_list = [nos_rule_par, nos_rule_par_mod, ocr_rule_par, ocrr_rule_par, nos_rule_trqx, nos_rule_trqx_mod, ocr_rule_trqx, ocrr_rule_trqx]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_par, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.multilisting_order.add_fields_into_repeating_group_algo('NoStrategyParameters', [['PostMode', '14', self.post_mode], ['VenueWeights', '14', self.venue_weight_par + '/' + self.venue_weight_trqx]])
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)
        # endregion

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order Paris
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order Paris", self.test_id))

        dma_1_order_par = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_order_par.change_parameters(dict(OrderQty=self.child_qty_par, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(dma_1_order_par, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA Paris order')

        pending_dma_1_order_par_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_par, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_par_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA Paris order')

        new_dma_1_order_par_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_par, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_par_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA Paris order')
        # endregion

        # region Check child DMA order TRQX
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order TRQX", self.test_id))

        dma_1_order_trqx = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_order_trqx.change_parameters(dict(OrderQty=self.child_qty_trqx, Price=self.price, Instrument=self.instrument, Account=self.account_trqx, ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(dma_1_order_trqx, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA TRQX order')

        pending_dma_1_order_trqx_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_trqx, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_trqx_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA TRQX order')

        new_dma_1_order_trqx_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_trqx, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_trqx_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA TRQX order')
        # endregion

        # region Modify parent multilisting order's qty
        case_id_2 = bca.create_event("Replace Multilisting Order - Qty", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.multilisting_order_replace_params_qty = FixMessageOrderCancelReplaceRequestAlgo(self.multilisting_order)
        self.multilisting_order_replace_params_qty.change_parameter('OrderQty', self.mod_qty)
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order_replace_params_qty, case_id_2)

        time.sleep(3)

        self.fix_verifier_sell.check_fix_message(self.multilisting_order_replace_params_qty, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        replaced_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params_qty, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(replaced_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region check OCRR PAR TRQX DMA child orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Modifying child order's quantities", self.test_id))

        # region check OCRR TRQX DMA child order
        replace_dma_1_order_trqx_trqx_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_trqx, self.gateway_side_buy, self.status_cancel_replace)
        replace_dma_1_order_trqx_trqx_params.change_parameter('OrderQty', self.mod_child_qty_par)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_trqx_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Replaced Child DMA TRQX order')
        # endregion

        # region check OCRR Paris DMA child order
        replace_dma_1_order_par_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_par, self.gateway_side_buy, self.status_cancel_replace)
        replace_dma_1_order_par_params.change_parameter('OrderQty', self.mod_child_qty_par)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_par_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Replaced Child DMA Paris order')
        # endregion
        # endregion

        time.sleep(3)

        # region Modify parent multilisting order's price
        self.fix_verifier_sell = FixVerifier(self.fix_env1.sell_side, self.test_id)
        case_id_3 = bca.create_event("Replace Multilisting Order - Price", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        self.multilisting_order_replace_params_price = FixMessageOrderCancelReplaceRequestAlgo(self.multilisting_order)
        self.multilisting_order_replace_params_price.change_parameters(dict(Price=self.mod_price, OrderQty=self.mod_qty))
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order_replace_params_price, case_id_3)

        time.sleep(6)
        self.fix_verifier_sell.check_fix_message(self.multilisting_order_replace_params_price, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        replaced_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params_price, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(replaced_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # # region check cancel of child DMA orders
        self.fix_verifier_buy.set_case_id(bca.create_event('Cancelling DMA orders Paris and TRQX', self.test_id))

        # region check cancel Paris DMA child order
        cancel_dma_1_order_par = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_par, self.gateway_side_buy, self.status_cancel)
        cancel_dma_1_order_par.change_parameter('OrderQty', self.mod_child_qty_par)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order_par, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel first DMA Paris order")
        # endregion

        # region check cancel TRQX DMA child order
        cancel_dma_1_order_trqx = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order_trqx, self.gateway_side_buy, self.status_cancel)
        cancel_dma_1_order_trqx.change_parameter('OrderQty', self.mod_child_qty_trqx)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order_trqx, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel first DMA TRQX order")
        # endregion
        # endregion
        
        # region check second Paris DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Paris Child DMA 2 order", self.test_id))

        self.dma_2_order_par = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_order_par.change_parameters(dict(OrderQty=self.mod_child_qty_par, Price=self.mod_price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order_par, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Paris Child DMA 2 order')

        time.sleep(2)

        pending_dma_2_order_par_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_par, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_2_order_par_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Paris Child DMA 2 order')

        new_dma_2_order_par_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_par, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_2_order_par_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Paris Child DMA 2 order')
        # endregion
        
        # region check second TRQX DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("TRQX Child DMA 2 order", self.test_id))

        self.dma_2_order_trqx = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_order_trqx.change_parameters(dict(OrderQty=self.mod_child_qty_trqx, Price=self.mod_price, Instrument=self.instrument, Account=self.account_trqx, ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order_trqx, key_parameters=self.key_params, message_name='Buy side NewOrderSingle TRQX Child DMA 2 order')

        time.sleep(2)

        pending_dma_2_order_trqx_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_trqx, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_2_order_trqx_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew TRQX Child DMA 2 order')

        new_dma_2_order_trqx_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_trqx, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_2_order_trqx_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New TRQX Child DMA 2 order')
        # endregion

        time.sleep(3)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_multilisting_order = FixMessageOrderCancelRequest(self.multilisting_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_multilisting_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        cancel_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params_price, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_multilisting_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion

        # region check cancel Paris and TRQX second DMA child orders
        self.fix_verifier_buy.set_case_id(bca.create_event('Cancelling Paris and TRQX second DMA child orders', self.test_id))

        # region check cancel Paris second DMA child order
        cancel_dma_2_order_par = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_par, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_2_order_par, self.key_params, self.ToQuod, "Buy Side ExecReport Paris Cancel child DMA 2 order")
        # endregion
        
        # region check cancel TRQX second DMA child order
        cancel_dma_2_order_trqx = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order_trqx, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_2_order_trqx, self.key_params, self.ToQuod, "Buy Side ExecReport TRQX Cancel child DMA 2 order")
        # endregion
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
