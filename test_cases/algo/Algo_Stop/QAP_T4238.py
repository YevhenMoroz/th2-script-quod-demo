import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.data_sets.constants import OrderSide, TimeInForce
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets.constants import OrderType

class QAP_T4238(TestCase):
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
        self.qty = 700
        self.display_qty = 100
        self.stop_px = 10
        self.price_ask = 10
        self.price_bid = 8
        self.qty_bid = self.qty_ask = 1_000_000
        self.order_type_stp = OrderType.Stop.value
        self.order_type_mkt = OrderType.Market.value
        self.tif_ioc = TimeInForce.ImmediateOrCancel.value
        self.side = OrderSide.Buy.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.Sell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel_replace = Status.CancelReplace
        self.status_eliminate = Status.Eliminate
        self.status_partfill = Status.PartialFill
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_36")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_43")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_24")
        self.listing = self.data_set.get_listing_id_by_name("listing_55")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_4")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_mkt_rule = rule_manager.add_NewOrdSingle_Market(self.fix_env1.buy_side, self.account, self.ex_destination_1, True, self.display_qty, self.stop_px)
        self.rule_list = [nos_mkt_rule]
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Send LTQ and Phase
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Trade", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.stop_px, MDEntrySize=self.display_qty)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for Stop order
        case_id_1 = bca.create_event("Create Stop Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.synthstop_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Stop_params()
        self.synthstop_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.synthstop_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, Side=self.side,
                                                    StopPx=self.stop_px, DisplayInstruction=dict(DisplayQty=self.display_qty), ExDestination=self.ex_destination_1))
        self.fix_manager_sell.send_message_and_receive_response(self.synthstop_order, case_id_1)
        # endregion

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        # region Send LTQ and Phase
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_incr_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing, self.fix_env1.feed_handler)
        market_data_incr_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.stop_px, MDEntrySize=self.display_qty)
        self.fix_manager_feed_handler.send_message(market_data_incr_par)
        # endregion

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.synthstop_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_synthstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthstop_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_synthstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_synthstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthstop_order, self.gateway_side_sell, self.status_new)
        new_synthstop_order_params.change_parameter('NoParty', '*')
        self.fix_verifier_sell.check_fix_message(new_synthstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        
        # region Check DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.dma_order.change_parameters(dict(Side=self.side, OrderQty=self.qty, Instrument=self.instrument, OrdType=self.order_type_mkt,
                                              Account=self.account, ExDestination=self.ex_destination_1, DisplayInstruction='*')).remove_parameter('Price')
        self.fix_verifier_buy.check_fix_message(self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA order')

        self.pending_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.pending_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA order')

        self.new_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(self.new_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA order')
        
        self.partfill_dma_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_partfill)
        self.partfill_dma_order_params.change_parameter('Price', self.price_ask)
        self.fix_verifier_buy.check_fix_message(self.partfill_dma_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PartFill Child DMA order')
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Eliminate Algo Order
        eliminate_synthstop_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.synthstop_order, self.gateway_side_sell, self.status_eliminate)
        self.fix_verifier_sell.check_fix_message(eliminate_synthstop_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Eliminate')
        # endregion

        # region check eliminate DMA passive child order
        self.er_eliminate_dma_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_eliminate)
        self.er_eliminate_dma_order.remove_parameter('Text')
        self.fix_verifier_buy.check_fix_message(self.er_eliminate_dma_order, self.key_params, self.ToQuod, "Buy Side ExecReport Eliminate DMA child order")
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
