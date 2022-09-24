import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager
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

class QAP_T4918(TestCase):
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
        self.delay = 10
        self.qty = 1000
        self.dec_qty = 60
        self.display_qty = self.dma1_qty = 50
        self.dma2_qty = 10
        self.price = 20
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1_000_000
        self.tif_day = constants.TimeInForce.Day.value
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
        self.status_fill = Status.Fill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_2")
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
        rule_manager = RuleManager()
        dma1_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQty(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price, self.price, self.dma1_qty, self.dma1_qty, self.delay)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest_ExecutionReport(self.fix_env1.buy_side, False)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [ocr_rule, ocrr_rule, dma1_trade_rule, nos_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for Iceberg order
        case_id_1 = bca.create_event("Create Iceberg Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.iceberg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Iceberg_params()
        self.iceberg_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.iceberg_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.iceberg_order.add_tag(dict(DisplayInstruction=dict(DisplayQty=self.display_qty)))

        self.fix_manager_sell.send_message_and_receive_response(self.iceberg_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.iceberg_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.iceberg_order, self.gateway_side_sell, self.status_pending)
        pending_iceberg_order_params.remove_parameter('NoParty')
        self.fix_verifier_sell.check_fix_message(pending_iceberg_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.iceberg_order, self.gateway_side_sell, self.status_new)
        new_iceberg_order_params.change_parameter('NoParty', '*').remove_parameter('SecondaryAlgoPolicyID')
        self.fix_verifier_sell.check_fix_message(new_iceberg_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_1_order.change_parameters(dict(OrderQty=self.dma1_qty, Price=self.price, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order')
        # endregion

        # region Modify parent iceberg order
        case_id_2 = bca.create_event("Replace Iceberg Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        self.iceberg_order_replace_params = FixMessageOrderCancelReplaceRequestAlgo(self.iceberg_order)
        self.iceberg_order_replace_params.change_parameter('OrderQty', self.dec_qty).add_tag(dict(DisplayInstruction=dict(DisplayQty=self.display_qty)))
        self.fix_manager_sell.send_message_and_receive_response(self.iceberg_order_replace_params, case_id_2)

        time.sleep(15)

        self.fix_verifier_sell.check_fix_message(self.iceberg_order_replace_params, direction=self.ToQuod, message_name='Sell side OrderCancelReplaceRequest')

        replaced_iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.iceberg_order_replace_params, self.gateway_side_sell, self.status_cancel_replace)
        replaced_iceberg_order_params.change_parameters(dict(NoParty='*'))
        self.fix_verifier_sell.check_fix_message(replaced_iceberg_order_params, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')
        # endregion

        # region Check Fill
        self.fix_verifier_buy.set_case_id(bca.create_event("Fill child Order", self.test_id))

        fill_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_fill)
        fill_dma_order.change_parameters(dict(CumQty=self.dma1_qty, LeavesQty=0, LastQty=self.dma1_qty, LastPx=self.price, Text='*'))
        self.fix_verifier_buy.check_fix_message(fill_dma_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Fill')

        time.sleep(20)
        # endregion

        # region check second DMA child order
        self.dma_2_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_2_order.change_parameters(dict(OrderQty=self.dma2_qty, Price=self.price, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_2_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 2 order')

        pending_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 2 order')

        new_dma_2_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_dma_2_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 2 order')
        # endregion

        # region check cancel second DMA child order
        cancel_dma_2_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_2_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_2_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel DMA order")
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_iceberg_order = FixMessageOrderCancelRequest(self.iceberg_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_iceberg_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_iceberg_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        cancel_iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.iceberg_order, self.gateway_side_sell, self.status_cancel)
        cancel_iceberg_order_params.change_parameters(dict(OrderQty=self.dec_qty, NoParty='*', SettlType='*', CxlQty=self.dma2_qty, CumQty=self.dma1_qty, AvgPx=self.price)).remove_parameters(['NoStrategyParameters', 'SecondaryAlgoPolicyID'])
        self.fix_verifier_sell.check_fix_message(cancel_iceberg_order_params, key_parameters=self.key_params, message_name='Sell side ExecReport Cancel')
        # endregion

        rule_manager = RuleManager()
        rule_manager.remove_rules(self.rule_list)