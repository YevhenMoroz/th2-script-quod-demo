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
        self.agr_price = 20
        self.side = constants.OrderSide.Sell.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.start_price_bid_par = 21
        self.start_qty_bid_par_and_trqx = 400
        self.start_price_bid_trqx_1 = 20
        self.start_price_bid_trqx_2 = 22
        self.start_qty_trqx_bid_1_2 = 400
        self.update_price_bid_par_trqx = 1
        self.update_qty_bid_par_trqx = 1
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
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
        self.qty_trqx = 800
        self.qty_par = 400
        self.qty_last_passive_child = self.qty - self.qty_par - self.qty_trqx
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_2 = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.account2 = self.data_set.get_account_by_name("account_5")
        self.s_par = self.data_set.get_listing_id_by_name("listing_2")
        self.s_trqx = self.data_set.get_listing_id_by_name("listing_3")
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
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.agr_price)
        self.ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        nos1_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account2, self.ex_destination_2, True, self.qty_trqx, self.agr_price)
        nos2_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.qty_par, 21)
        nos3_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account2, self.ex_destination_2, False, 0, 21.95)
        self.rule_list = [nos_1_rule, nos_2_rule, self.ocr_rule, nos1_ioc_rule, nos2_ioc_rule]
        # endregion

        # region Send MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=self.start_price_bid_par, MDEntrySize=self.start_qty_bid_par_and_trqx)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=self.start_price_bid_trqx_1, MDEntrySize=self.start_qty_bid_par_and_trqx)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryType=0, MDEntryPx=self.start_price_bid_trqx_2, MDEntrySize=self.start_qty_bid_par_and_trqx)
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

        pending_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA 1 order", self.test_id))

        dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_order.change_parameters(dict(Side=self.side, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message(dma_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport gNew Child DMA 1 order')
        # endregion

        # region Modify parent multilisting order
        case_id_2 = bca.create_event("Replace Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.multilisting_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.multilisting_order)
        self.multilisting_order_replace_params.change_parameters(dict(Price=self.agr_price))
        self.fix_manager_sell.send_message_and_receive_response(self.multilisting_order_replace_params, case_id_2)

        time.sleep(2)

        self.fix_verifier_sell.check_fix_message(self.multilisting_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        replaced_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        replaced_multilisting_order_params.add_tag(dict(SettlDate='*', SettlType='*')).remove_parameter('NoParty')
        self.fix_verifier_sell.check_fix_message(replaced_multilisting_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region check cancel first dma child order
        cancel_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_1_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel DMA 1 order")
        # endregion

        # region Update MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_spar = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_spar.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=19.95, MDEntrySize=10)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_spar)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Update Market Data", self.test_id))
        market_data_snap_shot_strqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_strqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryType=0, MDEntryPx=19.95, MDEntrySize=10)
        market_data_snap_shot_strqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryType=0, MDEntryPx=21.95, MDEntrySize=10)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_strqx)

        time.sleep(2)
        # endregion

        # region Agressive Orders
        case_id_3 = bca.create_event("Agressive orders", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)

        # region Check first aggressive DMA child order on venue TRQX with qty=800 and price=20
        self.fix_verifier_buy.set_case_id(bca.create_event("First DMA aggressive child", self.test_id))

        self.dma_2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_order.change_parameters(dict(Side=self.side, Account=self.account2, OrderQty=self.qty_trqx, Price=self.agr_price, Instrument=self.instrument, ExDestination=self.ex_destination_2, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle First DMA aggressive child')

        pending_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        pending_dma_2_order_params.change_parameters(dict(ExDestination=self.ex_destination_2))
        self.fix_verifier_buy.check_fix_message(pending_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew First DMA aggressive child')

        new_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        new_dma_2_order_params.change_parameters(dict(ExDestination=self.ex_destination_2))
        self.fix_verifier_buy.check_fix_message(new_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New First DMA aggressive child')
        # endregion

        # region Check Fill first DMA aggressive child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill first DMA aggressive child order", self.test_id))

        fill_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_fill)
        fill_dma_2_order.change_parameters(dict(CumQty=self.qty_trqx, LeavesQty=0, LastQty=self.qty_trqx, LastPx=self.agr_price, AvgPx=self.agr_price))
        self.fix_verifier_buy.check_fix_message(fill_dma_2_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill')
        # endregion

        # region Check second aggressive order on venue Paris with qty=400 and price=21
        self.fix_verifier_buy.set_case_id(bca.create_event("Second DMA aggressive child", self.test_id))

        self.dma_3_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_3_order.change_parameters(dict(Side=self.side, Account=self.account, OrderQty=self.qty_par, Price=21, Instrument=self.instrument, ExDestination=self.ex_destination_1, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message(self.dma_3_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Second DMA aggressive child')

        pending_dma_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Second DMA aggressive child')

        new_dma_3_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_3_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Second DMA aggressive child')
        # endregion

        # region Check Fill second DMA aggressive child order
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill second DMA aggressive child order", self.test_id))

        fill_dma_3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_3_order, self.gateway_side_buy, self.status_fill)
        fill_dma_3_order.change_parameters(dict(CumQty=self.qty_par, LeavesQty=0, LastQty=self.qty_par, LastPx=21, AvgPx=21))
        self.fix_verifier_buy.check_fix_message(fill_dma_3_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill')
        # endregion
        # endregion

        # region Check passive order on venue Paris with qty=100 and price=20
        self.fix_verifier_buy.set_case_id(bca.create_event("DMA passive child", self.test_id))

        self.dma_4_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_4_order.change_parameters(dict(Side=self.side, Account=self.account, OrderQty=self.qty_last_passive_child, Price=self.agr_price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.fix_verifier_buy.check_fix_message(self.dma_4_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA passive child')

        pending_dma_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA passive child')

        new_dma_4_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_4_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New DMA passive child')
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
        cancel_dma_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_4_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel passive DMA child order")
        # endregion

        cancel_multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.multilisting_order_replace_params, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_multilisting_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)





