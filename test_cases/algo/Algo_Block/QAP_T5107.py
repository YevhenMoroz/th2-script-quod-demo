import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase


class QAP_T5107(TestCase):
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
        self.qty = 1_000
        self.price = 30
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 10000
        self.release_mode = 'LastTradedQty'
        self.modify_factor = 1
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
        self.listing_id_par = self.data_set.get_listing_id_by_name("listing_1")
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
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        ocr_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account, self.ex_destination_1, True)
        self.rule_list = [ocr_rule, nos_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Set TradingPhase and LTQ for POV
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Set TradingPhase for POV", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_par, self.fix_env1.feed_handler)  # 1015
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntriesIR', MDEntryPx=self.price, MDEntrySize=self.qty)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Block order
        case_id_1 = bca.create_event("Create Synthetic Block Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Synthetic_Block_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Block_params()
        self.Synthetic_Block_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Synthetic_Block_order.update_repeating_group('NoStrategyParameters', [dict(StrategyParameterName='ReleaseMode', StrategyParameterType='14', StrategyParameterValue=self.release_mode),
                                                          dict(StrategyParameterName='ModifyFactor', StrategyParameterType='6', StrategyParameterValue=self.modify_factor)])
        self.Synthetic_Block_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.ex_destination_1))
        self.fix_manager_sell.send_message_and_receive_response(self.Synthetic_Block_order, case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.set_case_id(bca.create_event("Check Synthetic TIF order", self.test_id))
        self.fix_verifier_sell.check_fix_message(self.Synthetic_Block_order, self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Synthetic_Block_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Synthetic_Block_order, self.gateway_side_sell, self.status_pending)
        er_pending_new_Synthetic_Block_order_params.change_parameter('NoStrategyParameters', '*').remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(er_pending_new_Synthetic_Block_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        er_new_Synthetic_Block_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Synthetic_Block_order, self.gateway_side_sell, self.status_new)
        er_new_Synthetic_Block_order_params.change_parameters(dict(NoStrategyParameters='*')).remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(er_new_Synthetic_Block_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Check child orders", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_1, OrderQty=self.qty, Price=self.price, Instrument='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA')

        er_pending_new_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(er_pending_new_dma_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA')

        er_new_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(er_new_dma_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA')
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Synthetic TIF order
        case_id_2 = bca.create_event("Cancel Synthetic Block Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Synthetic_Block_order = FixMessageOrderCancelRequest(self.Synthetic_Block_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Synthetic_Block_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Synthetic_Block_order, direction=self.ToQuod, message_name='Sell side Cancel Request')
        # endregion

        # region Check that Synthetic Block order was canceled
        er_cancel_Synthetic_Block_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Synthetic_Block_order, self.gateway_side_sell, self.status_cancel)
        er_cancel_Synthetic_Block_order_params.change_parameters(dict(NoStrategyParameters='*')).remove_parameter('TargetStrategy')
        self.fix_verifier_sell.check_fix_message(er_cancel_Synthetic_Block_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion

        # check cancel child DMA
        cancel_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_dma_order, self.key_params, self.ToQuod, "Buy Side ExecReport Cancel Child DMA")
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)