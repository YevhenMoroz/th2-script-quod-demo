import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, StrategyParameterType
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants


class QAP_T4053(TestCase):
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
        self.qty_ask = 100
        self.qty_bid = 100
        self.price_bid = 13
        self.price_ask_1 = 15
        self.price_ask_2 = 20
        self.qty = 150
        self.qty_child_1 = 50
        self.qty_child_2 = 100
        self.price = 17
        self.tif_fok = constants.TimeInForce.FillOrKill.value
        self.tif_day = constants.TimeInForce.Day.value
        self.venue_qlv1 = "QLVENUE1" # without IOC support
        self.venue_qlv2 = "QLVENUE2" # without FOK support
        self.string_type = StrategyParameterType.String.value
        self.bool_type = StrategyParameterType.Boolean.value
        self.aggress_single_ioc_val = "Y"
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminate = Status.Eliminate
        self.status_cancel = Status.Cancel
        self.status_replace = Status.CancelReplace
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_36")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_41")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_22")
        self.listing_qlv1 = self.data_set.get_listing_id_by_name("listing_53")
        self.listing_qlv2 = self.data_set.get_listing_id_by_name("listing_54")
        # endregion

        # region Key parameters
        self.key_params_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_fok_rule = rule_manager.add_NewOrdSingle_FOK(self.fix_env1.buy_side, self.account, self.ex_destination_1, False, self.price_ask_1)
        nos_new_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [nos_fok_rule, ocr_rule, ocrr_rule, nos_new_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data QLVENUE2", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv2, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_2, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data QLVENUE1", self.test_id))
        market_data_snap_shot_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_qlv1, self.fix_env1.feed_handler)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_trqx)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Multilisting order
        case_id_1 = bca.create_event("Create Multilisting Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Multilisting_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Multilisting_params()
        self.Multilisting_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Multilisting_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.Multilisting_order.add_fields_into_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='AllowedVenues', StrategyParameterType=self.string_type, StrategyParameterValue=f'{self.venue_qlv1}/{self.venue_qlv2}'),
                                                                                         dict(StrategyParameterName="AggressiveSingleOrderOnImmediateOrCancel", StrategyParameterType=self.bool_type, StrategyParameterValue=self.aggress_single_ioc_val)])

        self.fix_manager_sell.send_message_and_receive_response(self.Multilisting_order, case_id_1)
        # endregion

        time.sleep(1)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Multilisting_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_Multilisting_order_params, key_parameters=self.key_params_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_Multilisting_order_params, key_parameters=self.key_params_parent, message_name='Sell side ExecReport New')
        # endregion

        time.sleep(2)

        # region Check child DMA order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order 1", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty_child_2, Price=self.price_ask_1, Instrument='*', TimeInForce=self.tif_fok))
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params_child, message_name='Buy side NewOrderSingle Child DMA order 1')

        er_pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_dma_order_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order')

        er_new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order')

        er_fill_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_eliminate)
        # er_fill_dma_order_params.change_parameters(dict(CumQty=self.qty_ask))
        self.fix_verifier_buy.check_fix_message(er_fill_dma_order_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport PartFill Child DMA order')
        # endregion

        # region Check child DMA order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order 2", self.test_id))

        self.dma_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params(False)
        self.dma_order_2.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty_child_1, Price=self.price, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_order_2, key_parameters=self.key_params_child, message_name='Buy side NewOrderSingle Child DMA order 2')

        er_pending_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_dma_order_2_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order 2')

        er_new_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order_2_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order 2')
        
        self.mod_dma_order_2 = FixMessageOrderCancelReplaceRequestAlgo(self.dma_order_2)
        self.mod_dma_order_2.change_parameters(dict(OrderQty=self.qty))
        self.fix_verifier_buy.check_fix_message(self.mod_dma_order_2, key_parameters=self.key_params_child, message_name='Buy side OCRR Child DMA order 2')

        er_mod_dma_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_replace)
        er_mod_dma_order_2_params.change_parameters(dict(OrderQty=self.qty))
        self.fix_verifier_buy.check_fix_message(er_mod_dma_order_2_params, key_parameters=self.key_params_child, direction=self.ToQuod, message_name='Buy side ExecReport Modified Child DMA order 2')
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_3 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        cancel_request_Multilisting_order = FixMessageOrderCancelRequest(self.Multilisting_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Multilisting_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_Multilisting_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        cancel_Multilisting_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Multilisting_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_Multilisting_order_params, key_parameters=self.key_params_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        # region check cancel second dma child order
        cancel_dma_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order_2, self.gateway_side_buy, self.status_cancel)
        cancel_dma_order_2.change_parameter("OrderQty", self.qty)
        self.fix_verifier_buy.check_fix_message(cancel_dma_order_2, self.key_params_child, self.ToQuod, "Buy Side ExecReport Cancel child DMA order 2")
        # endregion

