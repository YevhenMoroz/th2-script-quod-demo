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
from test_framework.data_sets import constants


class QAP_T4116(TestCase):
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
        self.qty = 1300
        self.price = 23
        self.dec_price = 20
        self.qty_for_trqx = 800
        self.price_bid_xpar = 21
        self.price_bid_1_trqx= 20
        self.price_bid_2_trqx = 22
        self.qty_bid = 400
        self.leaves_qty = self.qty - 3 * self.qty_bid
        self.side = constants.OrderSide.Sell.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_partial_fill = Status.PartialFill
        self.status_fill = Status.Fill
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
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_xpar = self.data_set.get_account_by_name("account_2")
        self.account_trqx = self.data_set.get_account_by_name("account_5")
        self.listing_id_xpar = self.data_set.get_listing_id_by_name("listing_2")
        self.listing_id_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.dec_price)
        nos_1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, True, self.qty_bid, self.price_bid_xpar)
        nos_2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, True, self.qty_for_trqx, self.price_bid_1_trqx)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_1_ioc_rule, nos_2_ioc_rule, ocr_rule]
        # endregion

        # region Send MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_xpar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_xpar, self.fix_env1.feed_handler)
        market_data_snap_shot_xpar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=self.price_bid_xpar, MDEntrySize=self.qty_bid)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_xpar)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=self.price_bid_1_trqx, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.add_fields_into_repeating_group('NoMDEntries', [dict(MDEntryType=0, MDEntryPx=self.price_bid_2_trqx, MDEntrySize=self.qty_bid, MDEntryPositionNo=2)])
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.multilisting_order.change_parameters(dict(Side=self.side, Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))

        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order, case_id_1)

        time.sleep(2)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check 1st DMA passive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("1st passive child DMA order", self.test_id))

        dma_1_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_xpar_order.change_parameters(dict(Side=self.side, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(dma_1_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_1_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(2)

        # region Modify parent multilisting order
        case_id_2 = bca.create_event("Replace Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.multilisting_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.multilisting_order)
        self.multilisting_order_replace_params.change_parameters(dict(Price=self.dec_price))
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order_replace_params, case_id_2)

        self.fix_verifier_sell.check_fix_message(self.multilisting_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        er_replaced_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell.check_fix_message(er_replaced_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region check cancel first dma child order
        er_cancel_dma_1_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_1_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel 1st passive DMA order")
        # endregion

        # region Check 1st aggressive DMA child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Aggressive childs", self.test_id))

        self.dma_trqx_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_trqx_order.change_parameters(dict(Side=self.side, Account=self.account_trqx, OrderQty=self.qty_for_trqx, Price=self.price_bid_1_trqx, Instrument=self.instrument, ExDestination=self.ex_destination_trqx, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_trqx_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 1st DMA aggressive child')

        er_pending_new_dma_trqx_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_trqx_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_trqx_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 1st DMA aggressive child')

        er_new_dma_trqx_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_trqx_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_trqx_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New 1st DMA aggressive child')

        er_fill_dma_trqx_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_trqx_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_trqx_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill 1st DMA aggressive child')
        # endregion

        # region Check 2nd aggressive DMA child order
        self.dma_2_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_xpar_order.change_parameters(dict(Side=self.side, Account=self.account_xpar, OrderQty=self.qty_bid, Price=self.price_bid_xpar, Instrument=self.instrument, ExDestination=self.ex_destination_xpar, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_2_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 2nd DMA aggressive child')

        er_pending_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew 2nd DMA aggressive child')

        er_new_dma_2_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_2_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New 2nd DMA aggressive child')

        er_fill_dma_2_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_xpar_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(er_fill_dma_2_xpar_order, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill 2nd DMA aggressive child')
        # endregion

        # region Check 2nd DMA passive child order
        self.fix_verifier_buy.set_case_id(bca.create_event("2nd passive child DMA order", self.test_id))

        self.dma_3_xpar_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_3_xpar_order.change_parameters(dict(Side=self.side, Account=self.account_xpar, OrderQty=self.leaves_qty, Price=self.dec_price, Instrument=self.instrument, ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(self.dma_3_xpar_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle 2nd DMA passive child')

        er_pending_new_dma_3_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_xpar_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_3_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport 2nd PendingNew DMA passive child')

        er_new_dma_3_xpar_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_xpar_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_3_xpar_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New 2nd DMA passive child')
        # endregion
        
        # region Check partial fill parent
        er_partial_fill_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params, self.gateway_side_sell, self.status_partial_fill)
        er_partial_fill_multilisting_order_params.change_parameter('SettlType', '*')
        self.fix_verifier_sell.check_fix_message(er_partial_fill_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Partial fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_4 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_4)
        cancel_request_multilisting_order = FixMessageOrderCancelRequest(self.multilisting_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_multilisting_order, case_id_4)
        self.fix_verifier_sell.check_fix_message(cancel_request_multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel DMA passive child order
        er_cancel_dma_3_xpar_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_xpar_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(er_cancel_dma_3_xpar_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Cancel 2nd passive DMA child order")
        # endregion

        er_cancel_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_multilisting_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        time.sleep(5)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)





