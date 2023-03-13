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


class QAP_T8796(TestCase):
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

        self.price_ltq = 135
        self.qty_ltq_1 = 20_000

        self.passive_pov_qty = AlgoFormulasManager.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)
        self.aggressive_pov_qty_1 = AlgoFormulasManager.get_pov_child_qty_on_ltq(self.percentage_volume, self.qty_ltq_1, self.qty)
        self.aggressive_pov_qty_2 = 4223
        self.aggressive_pov_qty_3 = 2423

        self.check_order_sequence = False
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
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
        ocr_rule_xpar = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocr_rule_trqx = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule_xpar, nos_rule_trqx, nos_ioc_rule_xpar, nos_ioc_rule_trqx, ocr_rule_xpar, ocr_rule_trqx]
        # endregion

        # region Send MarketData on XPAR
        case_id_0 = bca.create_event("Send MarketData", self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on PARIS", case_id_0))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        # region Send MarketData on TRQX
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on TURQUOISE", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental setup LastTrade on TURQUOISE", case_id_0))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=0, MDEntrySize=0)
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

        time.sleep(5)
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        # endregion

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(30)
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

        # region Create list of fix message for check_message_sequence
        # region Passive XPAR order
        passive_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.passive_pov_qty, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_new)
        # endregion

        # region Passive TRQX order
        passive_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.passive_pov_qty, Price=self.price_bid, Instrument='*', ExDestination=self.ex_destination_trqx))

        pending_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_new)
        # endregion

        # region Aggressive XPAR order
        ioc_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_1, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_1, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))

        pending_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_1, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check of 1st aggressive SOR order
        # region Check sequence of 2 Passive and 12 Aggressive POV child orders
        case_id_2 = bca.create_event("SOR 1. Check sequence of 2 Passive and 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy side NewOrderSingle Passive and Aggressive", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([passive_child_order_par_1, passive_child_order_trqx_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy Side Pending New Passive and Aggressive", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([pending_passive_child_order_par_1_params, pending_passive_child_order_trqx_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy Side New Passive and Aggressive", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([new_passive_child_order_par_1_params, new_passive_child_order_trqx_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_2))
        self.fix_verifier_buy.check_fix_message_sequence([eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_2 = FixVerifier(self.fix_env1.buy_side, self.test_id)
        # endregion
        
        # region Check that POV algo order doesn't generate any SOR aggressive child orders
        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", case_id_2))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", case_id_2))
        market_data_snap_shot_par_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=0, MDEntrySize=0)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par_trqx)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", case_id_2))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        time.sleep(30)

        # region Check sequence of the FIX message to confirm that POV algo doesn't generate new child orders
        case_id_3 = bca.create_event("SOR 0. Check that POV algo order doesn't generate aggressive SOR child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy side NewOrderSingle Passive and Aggressive", case_id_3))
        self.fix_verifier_buy.check_fix_message_sequence([passive_child_order_par_1, passive_child_order_trqx_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_par_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1, ioc_child_order_trqx_1], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy Side Pending New Passive and Aggressive", case_id_3))
        self.fix_verifier_buy.check_fix_message_sequence([pending_passive_child_order_par_1_params, pending_passive_child_order_trqx_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_par_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params, pending_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 14 child orders Buy Side New Passive and Aggressive", case_id_3))
        self.fix_verifier_buy.check_fix_message_sequence([new_passive_child_order_par_1_params, new_passive_child_order_trqx_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_par_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params, new_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_3))
        self.fix_verifier_buy.check_fix_message_sequence([eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_par_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params, eliminate_ioc_child_order_trqx_1_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_3 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", case_id_3))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", case_id_3))
        market_data_snap_shot_par_trqx = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_trqx, self.fix_env1.feed_handler)
        market_data_snap_shot_par_trqx.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_par_trqx.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par_trqx)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", case_id_3))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion
        # endregion

        time.sleep(60)

        # region Check of 2nd and the 3rd aggressive SOR order
        # region 2nd Aggressive XPAR order
        ioc_child_order_par_2 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_par_2.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_2, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region 2nd Aggressive TRQX order
        ioc_child_order_trqx_2 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_trqx_2.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_2, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))

        pending_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_eliminated)
        # endregion
        
        # region 3rd Aggressive XPAR order
        ioc_child_order_par_3 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_par_3.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_3, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))

        pending_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region 3rd Aggressive TRQX order
        ioc_child_order_trqx_3 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        ioc_child_order_trqx_3.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_3, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        pending_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_4 = bca.create_event("SOR 2. Check sequence of 24 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 24 child orders Buy side NewOrderSingle Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 24 child orders Buy Side Pending New Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 24 child orders Buy Side New Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 24 child orders Buy Side Eliminate Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        #time.sleep(15)
        case_id_5 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_5)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_5)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        cancel_pov_order.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion