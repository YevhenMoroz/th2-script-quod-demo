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


class QAP_T11294(TestCase):
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
        self.qty_for_partial_fill = 1000
        self.price = 38
        self.dark_price = 30
        self.traded_qty = 0
        self.qty_for_md = 1000
        self.price_ask_qdl1 = 44
        self.price_bid_qdl1 = 30
        self.price_ask_qdl2 = 40
        self.price_bid_qdl2 = 28
        self.delay = 0
        self.tif_iok = constants.TimeInForce.ImmediateOrCancel.value
        self.algopolicy = 'QA_Auto_SORPING_Spray_1'
        self.display_qty = 50
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_36")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_qlv1 = self.data_set.get_mic_by_name("mic_41")
        self.ex_destination_qlv2 = self.data_set.get_mic_by_name("mic_42")
        self.ex_destination_qlv3 = self.data_set.get_mic_by_name("mic_43")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_23")
        self.listing_qlv1 = self.data_set.get_listing_id_by_name("listing_53")
        self.listing_qlv2 = self.data_set.get_listing_id_by_name("listing_54")
        self.listing_qlv3 = self.data_set.get_listing_id_by_name("listing_55")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_ER_eliminate_or_cancel_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_2_child")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_qlv1, self.price)
        nos_2_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_qlv2, self.price)
        nos_3_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_qlv3, self.price)
        ocr_1_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_qlv1, True)
        ocr_2_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_qlv2, True)
        ocr_3_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_qlv3, True)
        self.rule_list = [nos_1_rule, nos_2_rule, nos_3_rule, ocr_1_rule, ocr_2_rule, ocr_3_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl1, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl1, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl2 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv2, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_qdl2, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl2.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_qdl2, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl2)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for SORPING order
        case_id_1 = bca.create_event("Create SORPING Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Multilisted_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.Multilisted_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisted_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument)).add_tag(dict(ClientAlgoPolicyID=self.algopolicy, DisplayInstruction=dict(DisplayQty=self.display_qty))).remove_parameter('NoStrategyParameters')

        self.fix_manager_sell.send_message_and_receive_response(self.Multilisted_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Multilisted_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Lit child DMA orders
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit child DMA orders", self.test_id))
        
        # region Check the 1st child DMA order
        self.dma_qlv1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qlv1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_qlv1, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qlv1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        er_pending_new_dma_qlv1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qlv1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport PendingNew Passive child DMA 1 order")
        
        er_new_dma_qlv1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qlv1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 1 order")
        # endregion

        # region Check the 2nd child DMA order
        self.dma_qlv2_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qlv2_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_qlv2, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qlv2_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_qlv2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qlv2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport PendingNew Passive child DMA 2 order")

        er_new_dma_qlv2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv2_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qlv2_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 2 order")
        # endregion
        
        # region Check the 3rd child DMA order
        self.dma_qlv3_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_qlv3_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_qlv3, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_qlv3_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 2 order')

        er_pending_new_dma_qlv3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv3_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_qlv3_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport PendingNew Passive child DMA 2 order")

        er_new_dma_qlv3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv3_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_qlv3_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 2 order")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Multilisted_order = FixMessageOrderCancelRequest(self.Multilisted_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Multilisted_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Multilisted_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancel first dma child order
        er_cancel_dma_qlv1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv1_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_qlv1_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 1 order")
        # endregion

        # region check cancel second dma child order
        er_cancel_dma_qlv2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv2_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_qlv2_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 2 order")
        # endregion

        # region check cancel third dma child order
        er_cancel_dma_qlv3_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_qlv3_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_kepler(er_cancel_dma_qlv3_order, self.key_params_ER_eliminate_or_cancel_child, self.ToQuod, "Buy Side ExecReport Cancel Passive child DMA 3 order")
        # endregion

        er_cancel_Multilisted_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisted_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(er_cancel_Multilisted_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
