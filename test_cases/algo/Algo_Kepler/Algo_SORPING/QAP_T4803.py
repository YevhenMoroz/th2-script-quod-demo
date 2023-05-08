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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo


class QAP_T4803(TestCase):
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
        self.qty = 500
        self.inc_qty = 1500
        self.leaves_qty = self.inc_qty - self.qty
        self.price = 18
        self.dark_price = 30
        self.qty_for_md = 1000
        self.price_ask = 40
        self.price_bid = 30
        self.delay_for_1st_trade = 1900
        self.iceberg_display_qty = 250
        self.cumQtyForReplaceRule = 500
        self.partial_fill_ord_status = constants.OrdStatus.PartiallyFilled.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_4.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_fill = Status.Fill
        self.status_cancel_replace = Status.CancelReplace
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_8")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_quodlit1 = self.data_set.get_mic_by_name("mic_10")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_qdl1 = self.data_set.get_listing_id_by_name("listing_4")
        self.listing_id_qdl2 = self.data_set.get_listing_id_by_name("listing_5")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_cancel_reject_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_trade_1_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, self.price, self.qty, self.qty, 1000)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, False, 2000)
        nos_trade_2_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, self.price, self.leaves_qty, self.leaves_qty, 1000)
        self.rule_list = [nos_rule, nos_trade_1_rule, ocrr_rule, nos_trade_2_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy))

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')
        # endregion

        # region Modify parent LitDark order
        case_id_2 = bca.create_event("Replace LitDark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.SORPING_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.SORPING_order)
        self.SORPING_order_replace_params.change_parameters(dict(OrderQty=self.inc_qty))
        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order_replace_params, case_id_2)

        time.sleep(1)

        self.fix_verifier_sell.check_fix_message(self.SORPING_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.set_case_id(bca.create_event("Check parent order", self.test_id))

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check the 1st Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("1st lit child DMA order", self.test_id))

        self.dma_1_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_1_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        er_new_dma_1_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')

        time.sleep(5)

        er_fill_dma_1_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_1_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA 1 order')
        # endregion

        time.sleep(8)

        # region Check that the modification request is rejected for the DMA child
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that the modification request is rejected for the DMA child", self.test_id))
        er_reject_replace_dma_1_qdl1_order = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.dma_1_qdl1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_replace_dma_1_qdl1_order, self.key_params_ER_cancel_reject_child, self.ToQuod, "Buy Side ExecReport RejectReplace 1st child DMA order")
        # endregion

        # region Check replace parent order
        self.fix_verifier_sell.set_case_id(bca.create_event("Check replace parent order", self.test_id))
        er_replaced_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        er_replaced_SORPING_order_params.change_parameters(dict(OrdStatus=self.partial_fill_ord_status))
        self.fix_verifier_sell.check_fix_message(er_replaced_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region Check the 2nd Lit child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("2nd lit child DMA order", self.test_id))

        self.dma_2_qdl1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_qdl1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.leaves_qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_qdl1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        er_new_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')

        er_fill_dma_2_qdl1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_qdl1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_2_qdl1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Fill Child DMA 2 order')
        # endregion

        # region Check fill parent order
        self.fix_verifier_sell.set_case_id(bca.create_event("Check fill parent order", self.test_id))
        er_fill_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.SORPING_order_replace_params, self.gateway_side_sell, self.status_fill)
        er_fill_SORPING_order_params.change_parameters(dict(CumQty=self.inc_qty, LastQty=self.qty_for_md))
        self.fix_verifier_sell.check_fix_message(er_fill_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell Side ExecReport Fill')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
