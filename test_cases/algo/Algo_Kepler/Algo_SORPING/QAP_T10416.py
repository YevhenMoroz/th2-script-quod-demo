import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.algo_formulas_manager import AlgoFormulasManager
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
from test_framework.read_log_wrappers.algo.ReadLogVerifierAlgo import ReadLogVerifierAlgo
from test_framework.read_log_wrappers.algo_messages.ReadLogMessageAlgo import ReadLogMessageAlgo


class QAP_T10416(TestCase):
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
        self.price = 20
        self.qty_for_md = 500
        self.price_ask = 40
        self.price_bid = 30
        self.delay = 0
        self.tig_gtc = constants.TimeInForce.GoodTillCancel.value
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
        # endregion

        # region Read log verifier params
        self.log_verifier_by_name_1 = constants.ReadLogVerifiers.log_319_check_exec_type.value
        self.read_log_verifier_1 = ReadLogVerifierAlgo(self.log_verifier_by_name_1, report_id)
        self.key_params_readlog_1 = self.data_set.get_verifier_key_parameters_by_name("key_params_log_319_check_exec_type")

        self.log_verifier_by_name_2 = constants.ReadLogVerifiers.log_319_updating_status.value
        self.read_log_verifier_2 = ReadLogVerifierAlgo(self.log_verifier_by_name_2, report_id)
        self.key_params_readlog_2 = self.data_set.get_verifier_key_parameters_by_name("key_params_read_log_check_updating_status_with_order_id")
        # endregion

        # region Compare message parameters
        self.old_status = constants.TransactionStatus.open.value
        self.new_status = constants.TransactionStatus.terminated.value
        self.exec_type = constants.ExecType.cancel_reject.value
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, self.price, self.price, self.qty, self.qty, 2000)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_quodlit1, False, 3000)
        self.rule_list = [nos_rule, nos_trade_rule, ocr_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_qdl1 = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_qdl1, self.fix_env1.feed_handler)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_for_md)
        market_data_snap_shot_qdl1.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_for_md)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_qdl1)

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
        self.SORPING_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, ClientAlgoPolicyID=self.algopolicy, Instrument=self.instrument, TimeInForce=self.tig_gtc))
        responce = self.fix_manager_sell.send_message_and_receive_response(self.SORPING_order, case_id_1)

        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_SORPING_order = FixMessageOrderCancelRequest(self.SORPING_order)

        self.fix_manager_sell.send_message(cancel_request_SORPING_order)
        self.fix_verifier_sell.check_fix_message(cancel_request_SORPING_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        parent_SORPING_order_id = responce[0].get_parameter('ExecID')
        parent_SORPING_order_id_list = list(parent_SORPING_order_id)
        parent_SORPING_order_id_list[-1] = 3
        synth_tif_algo_child_order_id = "".join(map(str, parent_SORPING_order_id_list))

        time.sleep(3)

        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.SORPING_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_SORPING_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.SORPING_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_SORPING_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check Lit passive child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Lit passive child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_Child_of_SORPING_Kepler_params()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_quodlit1, OrderQty=self.qty, Price=self.price))
        self.fix_verifier_buy.check_fix_message_kepler(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Passive Child DMA 1 order')

        er_pending_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message_kepler(er_pending_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Pending new Passive child DMA 1 order")

        er_new_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message_kepler(er_new_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport New Passive child DMA 1 order")

        er_fill_dma_1_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message_kepler(er_fill_dma_1_order, self.key_params_ER_child, self.ToQuod, "Buy Side ExecReport Fill Passive child DMA 1 order")

        er_reject_cancel_dma_1_order = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_reject)
        self.fix_verifier_buy.check_fix_message_kepler(er_reject_cancel_dma_1_order, self.key_params_ER_cancel_reject_child, self.ToQuod, "Buy Side OrderCancelRejectReport child DMA 1 order")
        # endregion

        # region Check Read log
        time.sleep(70)
        
        compare_message_1 = ReadLogMessageAlgo().set_compare_message_for_check_exec_type()
        compare_message_1.change_parameters(dict(OrdID=synth_tif_algo_child_order_id, ExecType=self.exec_type))

        compare_message_2 = ReadLogMessageAlgo().set_compare_message_for_check_updating_status()
        compare_message_2.change_parameters(dict(OrderId=synth_tif_algo_child_order_id, OldStatus=self.old_status, NewStatus=self.new_status))

        self.read_log_verifier_1.set_case_id(bca.create_event("ReadLog: Check that the SynthTIF received the CancelReject", self.test_id))
        self.read_log_verifier_1.check_read_log_message(compare_message_1, self.key_params_readlog_1)

        self.read_log_verifier_2.set_case_id(bca.create_event("ReadLog: Check that the SynthTIF algo was terminated", self.test_id))
        self.read_log_verifier_2.check_read_log_message(compare_message_2, self.key_params_readlog_2)
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
