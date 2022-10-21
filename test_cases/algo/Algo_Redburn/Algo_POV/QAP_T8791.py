import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager


class QAP_T8791(TestCase):
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
        self.order_type = constants.OrderType.Limit.value
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value

        self.price_ask = 135
        self.qty_ask = 20_000

        self.price_bid = 134
        self.qty_bid = 10_000

        self.percentage_volume = 10

        self.qty = 1_000_000
        self.price = 136

        self.price_ltq = 133
        self.qty_ltq_1 = 10_000

        self.passive_pov_qty = AlgoFormulasManager.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)
        self.aggressive_pov_qty = AlgoFormulasManager.get_pov_child_qty_on_ltq(self.percentage_volume, self.qty_ltq_1, self.qty)
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_cancel = Status.Cancel
        self.status_eliminated = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_5")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_xpar = self.data_set.get_mic_by_name("mic_1")
        self.ex_destination_trqx = self.data_set.get_mic_by_name("mic_2")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account_xpar = self.data_set.get_account_by_name("account_2")
        self.account_trqx = self.data_set.get_account_by_name("account_5")
        self.s_par = self.data_set.get_listing_id_by_name("listing_2")
        self.s_trqx = self.data_set.get_listing_id_by_name("listing_3")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_5")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule_xpar = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price_bid)
        nos_rule_trqx = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price_bid)
        nos_ioc_rule_xpar = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, False, 0, self.price_ask)
        nos_ioc_rule_trqx = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, False, 0, self.price_ask)
        ocr_rule_xpar = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, True)
        ocr_rule_trqx = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, True)
        self.rule_list = [nos_rule_xpar, nos_rule_trqx, nos_ioc_rule_xpar, nos_ioc_rule_trqx, ocr_rule_xpar, ocr_rule_trqx]
        # endregion

        # region Send MarketData on XPAR
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        # region Send MarketData on TRQX
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Fix verifier buy
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Redburn_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume))
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, case_id_1)

        time.sleep(20)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.pov_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        new_pov_order_params.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region Check passive child order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive PAR child order - 1", self.test_id))

        self.passive_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.passive_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.passive_pov_qty, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(self.passive_child_order_par_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child 1')

        pending_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_par_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_passive_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  Passive Child 1')

        new_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_par_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_passive_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  Passive Child 1')
        # endregion

        # region Check passive child order 1
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive TRQX child order - 1", self.test_id))

        self.passive_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        self.passive_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.passive_pov_qty, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(self.passive_child_order_trqx_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child 1')

        pending_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_trqx_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_passive_child_order_trqx_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  Passive Child 1')

        new_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_trqx_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_passive_child_order_trqx_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  Passive Child 1')
        # endregion

        # region Check Aggressive SOR child orders
        self.fix_verifier_buy.set_case_id(bca.create_event("IOC XPAR child order - 1", self.test_id))

        ioc_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=4445, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        self.fix_verifier_buy.check_fix_message(ioc_child_order_par_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle IOC Child 1')

        pending_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  IOC Child 1')

        new_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  IOC Child 1')

        eliminate_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_eliminated)
        self.fix_verifier_buy.check_fix_message(eliminate_ioc_child_order_par_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate IOC Child 1')


        self.fix_verifier_buy.set_case_id(bca.create_event("IOC TRQX child order - 1", self.test_id))

        ioc_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=4445, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        self.fix_verifier_buy.check_fix_message(ioc_child_order_trqx_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle IOC Child 1')

        pending_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_trqx_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  IOC Child 1')

        new_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(new_ioc_child_order_trqx_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  IOC Child 1')

        eliminate_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_eliminated)
        self.fix_verifier_buy.check_fix_message(eliminate_ioc_child_order_trqx_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Eliminate IOC Child 1')

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle IOC", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([ioc_child_order_par_1], [self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'))

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New IOC", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([pending_passive_child_order_par_1_params, pending_passive_child_order_trqx_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'))

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 child orders Buy Side New IOC", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([new_ioc_child_order_par_1_params], [self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'))
        # endregion

        # # region Clear Market Data
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to update the BestAsk", self.test_id))
        # market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask_1)
        # self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        #
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the WorsePrice behavior", self.test_id))
        # market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        # market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_2)
        # self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        #
        # time.sleep(3)
        # # endregion
        #
        # # region Check IOC child order 2
        # self.fix_verifier_buy.set_case_id(bca.create_event("IOC child order - 2", self.test_id))
        #
        # ioc_child_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        # ioc_child_order_2.change_parameters(dict(OrderQty=self.qty_aggressive_child_2, Price=self.price_ask_1, Instrument='*', TimeInForce=self.tif_ioc))
        # self.fix_verifier_buy.check_fix_message(ioc_child_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle IOC Child 2')
        #
        # pending_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(pending_ioc_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew  IOC Child 2')
        #
        # new_ioc_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(new_ioc_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  IOC Child 2')
        #
        # partial_fill_ioc_child_order_2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_2, self.gateway_side_buy, self.status_partial_fill)
        # partial_fill_ioc_child_order_2.change_parameters(dict(OrdType=self.order_type, TimeInForce=self.tif_ioc))
        # self.fix_verifier_buy.check_fix_message(partial_fill_ioc_child_order_2, self.key_params, self.ToQuod, "Buy Side ExecReport Partial Fill IOC Child 2")
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        #time.sleep(15)
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        cancel_pov_order.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion

        RuleManager(Simulators.algo).remove_rules(self.rule_list)