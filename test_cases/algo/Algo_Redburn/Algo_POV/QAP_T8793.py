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
from test_framework.fix_wrappers.algo.FixMessageOrderCancelReplaceRequestAlgo import FixMessageOrderCancelReplaceRequestAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager


class QAP_T8793(TestCase):
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

        self.price_bid_1 = 134
        self.qty_bid_1 = 10_000
        self.price_bid_2 = 134.5
        self.qty_bid_2 = 15_000

        self.percentage_volume = 10

        self.qty = 1_000_000
        self.reduced_qty = 900_000
        self.price = 136

        self.price_ltq = 135
        self.qty_ltq_1 = 20_000

        self.passive_pov_qty_1 = AlgoFormulasManager.get_pov_child_qty(self.percentage_volume, self.qty_bid_1, self.qty)
        self.passive_pov_qty_2 = AlgoFormulasManager.get_pov_child_qty(self.percentage_volume, self.qty_bid_2, self.qty)
        self.aggressive_pov_qty_1 = AlgoFormulasManager.get_pov_child_qty_on_ltq(self.percentage_volume, self.qty_ltq_1, self.qty)
        self.aggressive_pov_qty_2 = 4223
        self.aggressive_pov_qty_3 = 6223
        self.aggressive_pov_qty_4 = 8223
        self.aggressive_pov_qty_5 = 10223
        self.aggressive_pov_qty_6 = 12223
        self.aggressive_pov_qty_7 = 14223
        self.aggressive_pov_qty_8 = 16223
        self.aggressive_pov_qty_9 = 18223
        self.aggressive_pov_qty_10_par = 20000
        self.aggressive_pov_qty_10_trqx = 223

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
        self.status_cancel_replace = Status.CancelReplace
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
        nos_rule_xpar_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price_bid_1)
        nos_rule_xpar_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, self.price_bid_2)
        nos_rule_trqx_1 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price_bid_1)
        nos_rule_trqx_2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, self.price_bid_2)
        nos_ioc_rule_xpar = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_xpar, self.ex_destination_xpar, False, 0, self.price_ask)
        nos_ioc_rule_trqx = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account_trqx, self.ex_destination_trqx, False, 0, self.price_ask)
        ocr_rule_xpar = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocr_rule_trqx = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule_xpar_1, nos_rule_xpar_2, nos_rule_trqx_1, nos_rule_trqx_2, nos_ioc_rule_xpar, nos_ioc_rule_trqx, ocr_rule_xpar, ocr_rule_trqx]
        # endregion

        # region Send MarketData on XPAR
        case_id_0 = bca.create_event("Send MarketData", self.test_id)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot setup MarketDepth on PARIS", case_id_0))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid_1)
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
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid_1)
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

        # region Create list of fix message for check_message_sequence
        # region Passive XPAR order
        passive_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        passive_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.passive_pov_qty_1, Price=self.price_bid_1, Instrument='*', ExDestination=self.ex_destination_xpar))
        passive_child_order_par_1.add_tag(dict(Parties='*', QtyType=0))
        passive_child_order_par_1.remove_parameter('NoParty')

        pending_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_new)
        # endregion

        # region Passive TRQX order
        passive_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        passive_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.passive_pov_qty_1, Price=self.price_bid_1, Instrument='*', ExDestination=self.ex_destination_trqx))
        passive_child_order_trqx_1.add_tag(dict(Parties='*', QtyType=0))
        passive_child_order_trqx_1.remove_parameter('NoParty')

        pending_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_pending)

        new_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_new)
        # endregion

        # region Aggressive XPAR order
        ioc_child_order_par_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_1.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_1, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_1.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_1.remove_parameter('NoParty')

        pending_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_1, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_1 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_1.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_1, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_1.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_1.remove_parameter('NoParty')

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

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 2st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_2.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_2, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_2.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_2.remove_parameter('NoParty')

        pending_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_2, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_2.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_2, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_2.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_2.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_2, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_3 = bca.create_event("SOR 2. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_3))
        self.fix_verifier_buy_2.check_fix_message_sequence([ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_par_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2, ioc_child_order_trqx_2], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_3))
        self.fix_verifier_buy_2.check_fix_message_sequence([pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_par_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params, pending_ioc_child_order_trqx_2_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_3))
        self.fix_verifier_buy_2.check_fix_message_sequence([new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_par_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params, new_ioc_child_order_trqx_2_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_2.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_3))
        self.fix_verifier_buy_2.check_fix_message_sequence([eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_par_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params, eliminate_ioc_child_order_trqx_2_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_3 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 3st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_3 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_3.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_3, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_3.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_3.remove_parameter('NoParty')

        pending_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_3, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_3 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_3.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_3, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_3.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_3.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_3_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_3, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_4 = bca.create_event("SOR 3. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_par_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3, ioc_child_order_trqx_3], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_par_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params, pending_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_par_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params, new_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_3.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_4))
        self.fix_verifier_buy_3.check_fix_message_sequence([eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_par_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params, eliminate_ioc_child_order_trqx_3_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_4 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 4st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_4 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_4.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_4, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_4.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_4.remove_parameter('NoParty')

        pending_ioc_child_order_par_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_4, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_4, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_4, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_4 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_4.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_4, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_4.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_4.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_4, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_4, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_4_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_4, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_5 = bca.create_event("SOR 4. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_4.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_5))
        self.fix_verifier_buy_4.check_fix_message_sequence([ioc_child_order_par_4, ioc_child_order_par_4, ioc_child_order_par_4, ioc_child_order_par_4, ioc_child_order_par_4, ioc_child_order_par_4, ioc_child_order_trqx_4, ioc_child_order_trqx_4, ioc_child_order_trqx_4, ioc_child_order_trqx_4, ioc_child_order_trqx_4, ioc_child_order_trqx_4], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_4.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_5))
        self.fix_verifier_buy_4.check_fix_message_sequence([pending_ioc_child_order_par_4_params, pending_ioc_child_order_par_4_params, pending_ioc_child_order_par_4_params, pending_ioc_child_order_par_4_params, pending_ioc_child_order_par_4_params, pending_ioc_child_order_par_4_params, pending_ioc_child_order_trqx_4_params, pending_ioc_child_order_trqx_4_params, pending_ioc_child_order_trqx_4_params, pending_ioc_child_order_trqx_4_params, pending_ioc_child_order_trqx_4_params, pending_ioc_child_order_trqx_4_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_4.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_5))
        self.fix_verifier_buy_4.check_fix_message_sequence([new_ioc_child_order_par_4_params, new_ioc_child_order_par_4_params, new_ioc_child_order_par_4_params, new_ioc_child_order_par_4_params, new_ioc_child_order_par_4_params, new_ioc_child_order_par_4_params, new_ioc_child_order_trqx_4_params, new_ioc_child_order_trqx_4_params, new_ioc_child_order_trqx_4_params, new_ioc_child_order_trqx_4_params, new_ioc_child_order_trqx_4_params, new_ioc_child_order_trqx_4_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_4.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_5))
        self.fix_verifier_buy_4.check_fix_message_sequence([eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_par_4_params, eliminate_ioc_child_order_trqx_4_params, eliminate_ioc_child_order_trqx_4_params, eliminate_ioc_child_order_trqx_4_params, eliminate_ioc_child_order_trqx_4_params, eliminate_ioc_child_order_trqx_4_params, eliminate_ioc_child_order_trqx_4_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_5 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 5st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_5 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_5.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_5, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_5.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_5.remove_parameter('NoParty')

        pending_ioc_child_order_par_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_5, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_5, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_5, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_5 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_5.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_5, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_5.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_5.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_5, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_5, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_5_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_5, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Amend parent POV algo order
        self.fix_verifier_buy = FixVerifier(self.fix_env1.buy_side, self.test_id)
        case_id_5 = bca.create_event("Check cancel the first 2 passive child orders", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_5)

        self.fix_verifier_sell_2 = FixVerifier(self.fix_env1.sell_side, self.test_id)
        case_id_5 = bca.create_event("AMEND Parent order qty (reduce)", self.test_id)
        self.fix_verifier_sell_2.set_case_id(case_id_5)

        time.sleep(10)

        self.pov_order_reduced_qty = FixMessageOrderCancelReplaceRequestAlgo(self.pov_order)
        self.pov_order_reduced_qty.change_parameter('OrderQty', self.reduced_qty)
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order_reduced_qty, case_id_5)

        pov_order_replace_request = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.pov_order_reduced_qty, self.gateway_side_sell, self.status_cancel_replace)
        self.fix_verifier_sell_2.check_fix_message(pov_order_replace_request, key_parameters=self.key_params_cl, message_name='Sell Side ExecReport Replace Request')

        time.sleep(20)

        # region Check cancel first 2 passive child orders
        cancel_passive_child_order_xpar_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_passive_child_order_xpar_1_params, direction=self.ToQuod, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child XPAR 2')

        cancel_passive_child_order_trqx_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_passive_child_order_trqx_1_params, direction=self.ToQuod, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child XPAR 2')
        # endregion

        # region Check 2 new passive child orders
        # region Check XPAR passive child order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive child order XPAR - 2", self.test_id))

        passive_child_order_par_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        passive_child_order_par_2.change_parameters(dict(Account=self.account_xpar, OrderQty=self.passive_pov_qty_1, Price=self.price_bid_1, Instrument='*', ExDestination=self.ex_destination_xpar))
        passive_child_order_par_2.add_tag(dict(Parties='*', QtyType=0))
        passive_child_order_par_2.remove_parameter('NoParty')
        self.fix_verifier_buy.check_fix_message(passive_child_order_par_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child XPAR 2')

        pending_passive_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_passive_child_order_par_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child XPAR 2')

        new_passive_child_order_par_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_par_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_passive_child_order_par_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child XPAR 2')
        # endregion

        # region Check TRQX passive child order 2
        self.fix_verifier_buy.set_case_id(bca.create_event("Passive child order TRQX - 2", self.test_id))

        passive_child_order_trqx_2 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        passive_child_order_trqx_2.change_parameters(dict(Account=self.account_trqx, OrderQty=self.passive_pov_qty_1, Price=self.price_bid_1, Instrument='*', ExDestination=self.ex_destination_trqx))
        passive_child_order_trqx_2.add_tag(dict(Parties='*', QtyType=0))
        passive_child_order_trqx_2.remove_parameter('NoParty')
        self.fix_verifier_buy.check_fix_message(passive_child_order_trqx_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Passive Child TRQX 2')

        pending_passive_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(pending_passive_child_order_trqx_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Passive Child TRQX 2')

        new_passive_child_order_trqx_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_trqx_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(new_passive_child_order_trqx_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Passive Child TRQX 2')
        # endregion
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_6 = bca.create_event("SOR 5. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_5.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_6))
        self.fix_verifier_buy_5.check_fix_message_sequence([ioc_child_order_par_5, ioc_child_order_par_5, ioc_child_order_par_5, ioc_child_order_par_5, ioc_child_order_par_5, ioc_child_order_par_5, ioc_child_order_trqx_5, ioc_child_order_trqx_5, ioc_child_order_trqx_5, ioc_child_order_trqx_5, ioc_child_order_trqx_5, ioc_child_order_trqx_5], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_5.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_6))
        self.fix_verifier_buy_5.check_fix_message_sequence([pending_ioc_child_order_par_5_params, pending_ioc_child_order_par_5_params, pending_ioc_child_order_par_5_params, pending_ioc_child_order_par_5_params, pending_ioc_child_order_par_5_params, pending_ioc_child_order_par_5_params, pending_ioc_child_order_trqx_5_params, pending_ioc_child_order_trqx_5_params, pending_ioc_child_order_trqx_5_params, pending_ioc_child_order_trqx_5_params, pending_ioc_child_order_trqx_5_params, pending_ioc_child_order_trqx_5_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_5.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_6))
        self.fix_verifier_buy_5.check_fix_message_sequence([new_ioc_child_order_par_5_params, new_ioc_child_order_par_5_params, new_ioc_child_order_par_5_params, new_ioc_child_order_par_5_params, new_ioc_child_order_par_5_params, new_ioc_child_order_par_5_params, new_ioc_child_order_trqx_5_params, new_ioc_child_order_trqx_5_params, new_ioc_child_order_trqx_5_params, new_ioc_child_order_trqx_5_params, new_ioc_child_order_trqx_5_params, new_ioc_child_order_trqx_5_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_5.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_6))
        self.fix_verifier_buy_5.check_fix_message_sequence([eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_par_5_params, eliminate_ioc_child_order_trqx_5_params, eliminate_ioc_child_order_trqx_5_params, eliminate_ioc_child_order_trqx_5_params, eliminate_ioc_child_order_trqx_5_params, eliminate_ioc_child_order_trqx_5_params, eliminate_ioc_child_order_trqx_5_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_6 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 6st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_6 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_6.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_6, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_6.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_6.remove_parameter('NoParty')

        pending_ioc_child_order_par_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_6, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_6, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_6, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_6 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_6.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_6, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_6.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_6.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_6, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_6, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_6_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_6, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_7 = bca.create_event("SOR 6. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_6.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_7))
        self.fix_verifier_buy_6.check_fix_message_sequence([ioc_child_order_par_6, ioc_child_order_par_6, ioc_child_order_par_6, ioc_child_order_par_6, ioc_child_order_par_6, ioc_child_order_par_6, ioc_child_order_trqx_6, ioc_child_order_trqx_6, ioc_child_order_trqx_6, ioc_child_order_trqx_6, ioc_child_order_trqx_6, ioc_child_order_trqx_6], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_6.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_7))
        self.fix_verifier_buy_6.check_fix_message_sequence([pending_ioc_child_order_par_6_params, pending_ioc_child_order_par_6_params, pending_ioc_child_order_par_6_params, pending_ioc_child_order_par_6_params, pending_ioc_child_order_par_6_params, pending_ioc_child_order_par_6_params, pending_ioc_child_order_trqx_6_params, pending_ioc_child_order_trqx_6_params, pending_ioc_child_order_trqx_6_params, pending_ioc_child_order_trqx_6_params, pending_ioc_child_order_trqx_6_params, pending_ioc_child_order_trqx_6_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_6.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_7))
        self.fix_verifier_buy_6.check_fix_message_sequence([new_ioc_child_order_par_6_params, new_ioc_child_order_par_6_params, new_ioc_child_order_par_6_params, new_ioc_child_order_par_6_params, new_ioc_child_order_par_6_params, new_ioc_child_order_par_6_params, new_ioc_child_order_trqx_6_params, new_ioc_child_order_trqx_6_params, new_ioc_child_order_trqx_6_params, new_ioc_child_order_trqx_6_params, new_ioc_child_order_trqx_6_params, new_ioc_child_order_trqx_6_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_6.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_7))
        self.fix_verifier_buy_6.check_fix_message_sequence([eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_par_6_params, eliminate_ioc_child_order_trqx_6_params, eliminate_ioc_child_order_trqx_6_params, eliminate_ioc_child_order_trqx_6_params, eliminate_ioc_child_order_trqx_6_params, eliminate_ioc_child_order_trqx_6_params, eliminate_ioc_child_order_trqx_6_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_7 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 7st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_7 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_7.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_7, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_7.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_7.remove_parameter('NoParty')

        pending_ioc_child_order_par_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_7, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_7, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_7, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_7 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_7.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_7, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_7.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_7.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_7, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_7, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_7_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_7, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_8 = bca.create_event("SOR 7. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_7.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_8))
        self.fix_verifier_buy_7.check_fix_message_sequence([ioc_child_order_par_7, ioc_child_order_par_7, ioc_child_order_par_7, ioc_child_order_par_7, ioc_child_order_par_7, ioc_child_order_par_7, ioc_child_order_trqx_7, ioc_child_order_trqx_7, ioc_child_order_trqx_7, ioc_child_order_trqx_7, ioc_child_order_trqx_7, ioc_child_order_trqx_7], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_7.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_8))
        self.fix_verifier_buy_7.check_fix_message_sequence([pending_ioc_child_order_par_7_params, pending_ioc_child_order_par_7_params, pending_ioc_child_order_par_7_params, pending_ioc_child_order_par_7_params, pending_ioc_child_order_par_7_params, pending_ioc_child_order_par_7_params, pending_ioc_child_order_trqx_7_params, pending_ioc_child_order_trqx_7_params, pending_ioc_child_order_trqx_7_params, pending_ioc_child_order_trqx_7_params, pending_ioc_child_order_trqx_7_params, pending_ioc_child_order_trqx_7_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_7.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_8))
        self.fix_verifier_buy_7.check_fix_message_sequence([new_ioc_child_order_par_7_params, new_ioc_child_order_par_7_params, new_ioc_child_order_par_7_params, new_ioc_child_order_par_7_params, new_ioc_child_order_par_7_params, new_ioc_child_order_par_7_params, new_ioc_child_order_trqx_7_params, new_ioc_child_order_trqx_7_params, new_ioc_child_order_trqx_7_params, new_ioc_child_order_trqx_7_params, new_ioc_child_order_trqx_7_params, new_ioc_child_order_trqx_7_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_7.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_8))
        self.fix_verifier_buy_7.check_fix_message_sequence([eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_par_7_params, eliminate_ioc_child_order_trqx_7_params, eliminate_ioc_child_order_trqx_7_params, eliminate_ioc_child_order_trqx_7_params, eliminate_ioc_child_order_trqx_7_params, eliminate_ioc_child_order_trqx_7_params, eliminate_ioc_child_order_trqx_7_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_8 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 8st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_8 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_8.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_8, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_8.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_8.remove_parameter('NoParty')

        pending_ioc_child_order_par_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_8, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_8, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_8, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_8 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_8.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_8, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_8.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_8.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_8, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_8, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_8_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_8, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_9 = bca.create_event("SOR 8. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_8.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_9))
        self.fix_verifier_buy_8.check_fix_message_sequence([ioc_child_order_par_8, ioc_child_order_par_8, ioc_child_order_par_8, ioc_child_order_par_8, ioc_child_order_par_8, ioc_child_order_par_8, ioc_child_order_trqx_8, ioc_child_order_trqx_8, ioc_child_order_trqx_8, ioc_child_order_trqx_8, ioc_child_order_trqx_8, ioc_child_order_trqx_8], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_8.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_9))
        self.fix_verifier_buy_8.check_fix_message_sequence([pending_ioc_child_order_par_8_params, pending_ioc_child_order_par_8_params, pending_ioc_child_order_par_8_params, pending_ioc_child_order_par_8_params, pending_ioc_child_order_par_8_params, pending_ioc_child_order_par_8_params, pending_ioc_child_order_trqx_8_params, pending_ioc_child_order_trqx_8_params, pending_ioc_child_order_trqx_8_params, pending_ioc_child_order_trqx_8_params, pending_ioc_child_order_trqx_8_params, pending_ioc_child_order_trqx_8_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_8.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_9))
        self.fix_verifier_buy_8.check_fix_message_sequence([new_ioc_child_order_par_8_params, new_ioc_child_order_par_8_params, new_ioc_child_order_par_8_params, new_ioc_child_order_par_8_params, new_ioc_child_order_par_8_params, new_ioc_child_order_par_8_params, new_ioc_child_order_trqx_8_params, new_ioc_child_order_trqx_8_params, new_ioc_child_order_trqx_8_params, new_ioc_child_order_trqx_8_params, new_ioc_child_order_trqx_8_params, new_ioc_child_order_trqx_8_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_8.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_9))
        self.fix_verifier_buy_8.check_fix_message_sequence([eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_par_8_params, eliminate_ioc_child_order_trqx_8_params, eliminate_ioc_child_order_trqx_8_params, eliminate_ioc_child_order_trqx_8_params, eliminate_ioc_child_order_trqx_8_params, eliminate_ioc_child_order_trqx_8_params, eliminate_ioc_child_order_trqx_8_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_9 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 9st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_9 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_9.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_9, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_9.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_9.remove_parameter('NoParty')

        pending_ioc_child_order_par_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_9, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_9, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_9, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_9 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_9.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_9, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_9.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_9.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_9, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_9, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_9_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_9, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_10 = bca.create_event("SOR 9. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_9.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_10))
        self.fix_verifier_buy_9.check_fix_message_sequence([ioc_child_order_par_9, ioc_child_order_par_9, ioc_child_order_par_9, ioc_child_order_par_9, ioc_child_order_par_9, ioc_child_order_par_9, ioc_child_order_trqx_9, ioc_child_order_trqx_9, ioc_child_order_trqx_9, ioc_child_order_trqx_9, ioc_child_order_trqx_9, ioc_child_order_trqx_9], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_9.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_10))
        self.fix_verifier_buy_9.check_fix_message_sequence([pending_ioc_child_order_par_9_params, pending_ioc_child_order_par_9_params, pending_ioc_child_order_par_9_params, pending_ioc_child_order_par_9_params, pending_ioc_child_order_par_9_params, pending_ioc_child_order_par_9_params, pending_ioc_child_order_trqx_9_params, pending_ioc_child_order_trqx_9_params, pending_ioc_child_order_trqx_9_params, pending_ioc_child_order_trqx_9_params, pending_ioc_child_order_trqx_9_params, pending_ioc_child_order_trqx_9_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_9.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_10))
        self.fix_verifier_buy_9.check_fix_message_sequence([new_ioc_child_order_par_9_params, new_ioc_child_order_par_9_params, new_ioc_child_order_par_9_params, new_ioc_child_order_par_9_params, new_ioc_child_order_par_9_params, new_ioc_child_order_par_9_params, new_ioc_child_order_trqx_9_params, new_ioc_child_order_trqx_9_params, new_ioc_child_order_trqx_9_params, new_ioc_child_order_trqx_9_params, new_ioc_child_order_trqx_9_params, new_ioc_child_order_trqx_9_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_9.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_10))
        self.fix_verifier_buy_9.check_fix_message_sequence([eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_par_9_params, eliminate_ioc_child_order_trqx_9_params, eliminate_ioc_child_order_trqx_9_params, eliminate_ioc_child_order_trqx_9_params, eliminate_ioc_child_order_trqx_9_params, eliminate_ioc_child_order_trqx_9_params, eliminate_ioc_child_order_trqx_9_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        self.fix_verifier_buy_10 = FixVerifier(self.fix_env1.buy_side, self.test_id)

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check of 10st aggressive SOR order
        # region Aggressive XPAR order
        ioc_child_order_par_10 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_par_10.change_parameters(dict(Account=self.account_xpar, OrderQty=self.aggressive_pov_qty_10_par, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_xpar))
        ioc_child_order_par_10.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_par_10.remove_parameter('NoParty')

        pending_ioc_child_order_par_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_10, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_par_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_10, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_par_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_par_10, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Aggressive TRQX order
        ioc_child_order_trqx_10 = FixMessageNewOrderSingleAlgo().set_DMA_params()
        ioc_child_order_trqx_10.change_parameters(dict(Account=self.account_trqx, OrderQty=self.aggressive_pov_qty_10_trqx, Price=self.price_ask, TimeInForce=self.tif_ioc, Instrument='*', ExDestination=self.ex_destination_trqx))
        ioc_child_order_trqx_10.add_tag(dict(Parties='*', QtyType=0))
        ioc_child_order_trqx_10.remove_parameter('NoParty')

        pending_ioc_child_order_trqx_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_10, self.gateway_side_buy, self.status_pending)

        new_ioc_child_order_trqx_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_10, self.gateway_side_buy, self.status_new)

        eliminate_ioc_child_order_trqx_10_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(ioc_child_order_trqx_10, self.gateway_side_buy, self.status_eliminated)
        # endregion

        # region Check sequence of 12 Aggressive POV child orders
        case_id_11 = bca.create_event("SOR 10. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion

        # region Send MarketData to trigger the POV SOR Aggressive order creation
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to trigger the POV Aggressive order creation", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.s_par, self.fix_env1.feed_handler)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(20)
        # endregion
        # endregion

        # region Check that parent POV algo doesn't generate new SOR Aggressive child order
        # region Check sequence of 12 Aggressive POV child orders
        case_id_11 = bca.create_event("Check that algo doesn't generate new SOR order. Check sequence of 12 Aggressive POV child orders", self.test_id)
        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy side NewOrderSingle Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_par_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10, ioc_child_order_trqx_10], [self.key_params, self.key_params, self.key_params,self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.FromQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_D'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side Pending New Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_par_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params, pending_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_pending_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side New Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_par_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params, new_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_new'), check_order=self.check_order_sequence)

        self.fix_verifier_buy_10.set_case_id(bca.create_event("Check 12 child orders Buy Side Eliminate Aggressive", case_id_11))
        self.fix_verifier_buy_10.check_fix_message_sequence([eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_par_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params, eliminate_ioc_child_order_trqx_10_params], [self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params, self.key_params], self.ToQuod, pre_filter=self.data_set.get_pre_filter('pre_filer_equal_ER_eliminate'), check_order=self.check_order_sequence)
        # endregion
        # endregion

        # region Check eliminated Algo Order
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_order_cancel_replace(self.pov_order_reduced_qty, self.gateway_side_sell, self.status_cancel)
        cancel_pov_order.remove_parameter('SecAltIDGrp')
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, direction=self.FromQuod, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        RuleManager(Simulators.algo).remove_rules(self.rule_list)