import os
import time
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, OrderSide, TimeInForce
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.algo_formulas_manager import AlgoFormulasManager
from test_framework.core.test_case import TestCase


class QAP_T7728(TestCase):
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

        # region listing parameters
        self.cost_per_trade = 0
        self.comm_per_unit = 12
        self.comm_basis_points = 16
        self.spread_discount_proportion = 0
        self.is_comm_per_unit = False
        # endregion

        # region order parameters
        self.tif_ioc = TimeInForce.ImmediateOrCancel.value
        self.side = OrderSide.Buy.value
        self.qty = 1_000_000
        self.price = 70
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1_000_000
        self.visibility = 1
        self.imbalance_tolerance = 0
        self.dma_ord_px = AlgoFormulasManager.get_litdark_child_price(self.side, self.price_bid, self.price_ask, self.qty, self.cost_per_trade,
                                                                          self.comm_per_unit, self.comm_basis_points, self.is_comm_per_unit,
                                                                          self.spread_discount_proportion)
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
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_36")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.s_lit = self.data_set.get_listing_id_by_name("listing_53")
        self.ex_destination_dark = self.data_set.get_mic_by_name("mic_44")
        self.account = self.data_set.get_account_by_name("account_25")
        self.client = self.data_set.get_client_by_name("client_2")
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
        nos_ioc_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.ex_destination_dark, True, self.qty, self.dma_ord_px)
        self.rule_list = [nos_ioc_rule]
        # endregion

        time.sleep(5)

        # region Send_MarkerData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_lit, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # endregion

        time.sleep(3)

        # region Send NewOrderSingle (35=D) for LitDark order
        case_id_1 = bca.create_event("Create Multilisting LitDark Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.litdark_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_LitDark_params()
        self.litdark_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.litdark_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.litdark_order.add_fields_into_repeating_group_algo('NoStrategyParameters', [['Visibility', 6, self.visibility], ['ImbalanceTolerance', 6, self.imbalance_tolerance]])

        self.fix_manager_sell.send_message_and_receive_response(self.litdark_order, case_id_1)
        # endregion

        time.sleep(3)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.litdark_order, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_litdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.litdark_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_litdark_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_litdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.litdark_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_litdark_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        dma_1_order = FixMessageNewOrderSingleAlgo().set_DMA_params()
        dma_1_order.change_parameters(dict(Price=self.dma_ord_px, Instrument=self.instrument, OrderQty=self.qty, Account=self.account, TimeInForce=self.tif_ioc, ExDestination=self.ex_destination_dark))
        self.fix_verifier_buy.check_fix_message(dma_1_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child DMA 1 order')

        pending_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        
        fill_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_1_order, self.gateway_side_buy, self.status_fill)
        self.fix_verifier_buy.check_fix_message(fill_dma_1_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Filled Child DMA 1 order')
        # endregion

        time.sleep(5)

        # region check parent order filled
        fill_litdark_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.litdark_order, self.gateway_side_sell, self.status_fill)
        self.fix_verifier_sell.check_fix_message(fill_litdark_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Filled')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
