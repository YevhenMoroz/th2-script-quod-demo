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
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo


# Warning! This is the manual test case. It needs to do manual and doesn`t include in regression script
class QAP_T4082(TestCase):
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
        self.qty = 1500
        self.dec_qty = 1100
        self.remaining_qty = 500
        self.passive_child_qty = 1000
        self.price = 45
        self.traded_qty = 0
        self.qty_for_md = 500
        self.price_ask_qdl1 = 44
        self.price_bid = 30
        self.price_ask_qdl2 = 50
        self.delay = 2000
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = constants.ClientAlgoPolicy.qa_sorping_4.value
        self.ordtype = constants.OrderType.Market.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_fill = Status.Fill
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        self.status_reject = Status.Reject
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
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        self.key_params_ER_cancel_reject_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        self.key_params_ER_eliminate_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        self.key_params_specific_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_Eliminate_child")
        # endregion

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_ER_canceled")

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, False, self.traded_qty, self.price_ask_qdl1, 1000)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, self.price, self.passive_child_qty, self.passive_child_qty, self.delay)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, True)
        self.rule_list = [nos_ioc_rule, nos_rule, nos_trade_rule, ocrr_rule, ocr_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=30, MDEntrySize=0)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=40, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=30, MDEntrySize=0)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=40, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl3 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID('116017192', self.fix_env1.feed_handler)
        market_data_snap_shot_qdl3.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=30, MDEntrySize=0)
        market_data_snap_shot_qdl3.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=40, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.SORPING_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_SORPING_Kepler_params()
        self.SORPING_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, ClientAlgoPolicyID=self.algopolicy, OrdType=self.ordtype)).remove_parameter('Price')

        self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        time.sleep(1)

        time.sleep(1)

        self.nos_eliminate_rule = rule_manager.add_NewOrderSingle_ExecutionReport_Eliminate(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, 3000)

        time.sleep(2)

        rule_manager.remove_rule(self.nos_eliminate_rule)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Lit aggressive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit aggressive child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.remaining_qty, Price=self.price_ask_qdl1, TimeInForce=self.tif_ioc))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Aggressive Child DMA 1 order')

        er_pending_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Aggressive child DMA 1 order")

        er_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Aggressive child DMA 1 order")

        self.er_eliminate_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_eliminate)
        self.fix_verifier_buy.check_fix_message_kepler(self.er_eliminate_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Eliminate Aggressive child DMA 1 order")
        # endregion

        # region Check Lit passive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit passive child DMA orders", self.test_id))

        self.dma_2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.passive_child_qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 2 order')

        er_pending_new_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Passive child DMA 2 order")

        er_new_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 2 order")

        er_fill_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Passive child DMA 2 order")

        er_reject_replaced_dma_2_order_order_params = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_replaced_dma_2_order_order_params, self.key_params_ER_cancel_reject_child, self.ToQuod, 'Buy Side OrderCancelRejectReport child DMA 2 order')
        # endregion

        time.sleep(3)

        # region Check recycling Qty after fill previous child
        self.dma_3_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_3_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.remaining_qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_3_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 3 order')

        self.er_eliminate_dma_3_order = FixMessageExecutionReportAlgo().set_params_for_nos_eliminate_rule(self.dma_3_order)
        self.fix_verifier_buy.check_fix_message_kepler(self.er_eliminate_dma_3_order, self.key_params_ER_eliminate_child, self.ToQuod, "Buy Side ExecReport Eliminate Passive child DMA 3 order")
        # endregion

        # region Check recycling Qty after the elimination of previous child
        self.dma_4_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_4_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.remaining_qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_4_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 4 order')

        er_pending_new_dma_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_4_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Passive child DMA 4 order")

        er_new_dma_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_4_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 4 order")
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        # case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        # self.fix_verifier_sell.set_case_id(case_id_2)
        # cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)
        #
        # self.fix_manager_sell.send_message_and_receive_response(cancel_request_SORPING_order, case_id_2)
        # self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        #
        # # region ER cancel third dma child order
        # er_cancel_dma_4_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_4_order, self.gateway_side_buy, self.status_cancel)
        # # endregion
        #
        # # region Check that ER cancel for last child order exists
        # self.fix_verifier_buy.set_case_id(bca.create_event("Check that 2 DMA orders on qdl1 were eliminated and 1 was canceled", self.test_id))
        # self.fix_verifier_buy.check_fix_message_sequence([self.er_eliminate_dma_1_order, self.er_eliminate_dma_3_order, er_cancel_dma_4_order], key_parameters_list=[None, None, None], direction=self.ToQuod, pre_filter=self.pre_filter)
        # # endregion
        #
        # er_cancel_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_cancel)
        # self.fix_verifier_sell.check_fix_message(er_cancel_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
