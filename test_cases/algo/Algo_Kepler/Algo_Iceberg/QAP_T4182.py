import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets import constants
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.fix_wrappers.algo.FixMessageOrderCancelRejectReportAlgo import FixMessageOrderCancelRejectReportAlgo
from test_framework.algo_formulas_manager import AlgoFormulasManager


class QAP_T4182(TestCase):
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
        self.display_qty = 500
        self.price_ask = 40
        self.price_bid = 30
        self.qty_bid = self.qty_ask = 1000000
        self.px_for_incr = 0
        self.qty_for_incr = 0
        self.tif_gtd = constants.TimeInForce.GoodTillDate.value

        now = datetime.today() - timedelta(hours=3)
        delta = 5
        expire_date = (now + timedelta(days=delta))
        self.ExpireDate_for_sending = expire_date.strftime("%Y%m%d")
        shift = AlgoFormulasManager.make_expire_date_friday_if_it_is_on_weekend(expire_date)
        self.ExpireDate = (expire_date - timedelta(days=shift)).strftime("%Y%m%d")
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.Buy
        self.gateway_side_sell = GatewaySide.KeplerSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_9")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_paris = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_4")
        self.account = self.data_set.get_account_by_name("account_9")
        self.listing_id_paris = self.data_set.get_listing_id_by_name("listing_6")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_NOS_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_cancel_reject_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_child")
        self.key_params_ER_cancel_reject_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_cancel_reject_parent")
        self.key_params_ER_for_check_sequence = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_er_fill")
        # endregion

        self.rule_list = []

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_1_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_paris, self.price)
        self.rule_list = [nos_1_rule]
        # endregion

        # region Send_MarketData
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data", self.test_id))
        market_data_snap_shot_paris = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id_paris, self.fix_env1.feed_handler)
        market_data_snap_shot_paris.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid)
        market_data_snap_shot_paris.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_paris)

        market_data_snap_shot_paris = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_paris, self.fix_env1.feed_handler)
        market_data_snap_shot_paris.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_paris)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create Iceberg Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.Iceberg_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_Iceberg_Kepler()
        self.Iceberg_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.Iceberg_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, Instrument=self.instrument, ExDestination=self.ex_destination_paris, Price=self.price, TimeInForce=self.tif_gtd, DisplayInstruction=dict(DisplayQty=self.display_qty))).add_tag(dict(ExpireDate=self.ExpireDate))

        self.fix_manager_sell.send_message_and_receive_response(self.Iceberg_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.Iceberg_order, self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(er_pending_new_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new_Iceberg_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(er_new_Iceberg_order_params, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion

        # region Check 1st child DMA order
        self.fix_verifier_buy.set_case_id(bca.create_event("Child DMA order", self.test_id))

        self.dma_1_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_child_of_Iceberg_Kepler()
        self.dma_1_order.change_parameters(dict(Account=self.account, ExDestination=self.ex_destination_paris, OrderQty=self.display_qty, Price=self.price, Instrument=self.instrument, TimeInForce=self.tif_gtd)).add_tag(dict(ExpireDate='*'))
        self.fix_verifier_buy.check_fix_message(self.dma_1_order, key_parameters=self.key_params_NOS_child, message_name='Buy side NewOrderSingle Child DMA 1 order')

        self.er_pending_new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(self.er_pending_new_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child DMA 1 order')

        self.er_new_dma_1_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_1_order, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(self.er_new_dma_1_order_params, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New Child DMA 1 order')
        # endregion

        time.sleep(5)

        # region Set up Closing phase
        market_data_snap_shot_paris = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_paris, self.fix_env1.feed_handler)
        market_data_snap_shot_paris.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr, TradingSessionSubID='1')
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_paris)
        # endregion

        time.sleep(5)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)
        cancel_request_Iceberg_order = FixMessageOrderCancelRequest(self.Iceberg_order)

        self.fix_manager_sell.send_message_and_receive_response(cancel_request_Iceberg_order, case_id_2)
        self.fix_verifier_sell.check_fix_message(cancel_request_Iceberg_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        er_cancel_reject_Iceberg_order_params = FixMessageOrderCancelRejectReportAlgo().set_params_from_new_order_single(self.Iceberg_order, self.gateway_side_sell, self.status_new)
        er_cancel_reject_Iceberg_order_params.change_parameters(dict(Text="market has closed")).add_tag(dict(SecondaryAlgoPolicyID='*'))
        self.fix_verifier_sell.check_fix_message(er_cancel_reject_Iceberg_order_params, key_parameters=self.key_params_ER_cancel_reject_parent, message_name='Sell side ExecReport Cancel')
        # endregion

        time.sleep(5)

        # region Check that child has Open status
        self.fix_verifier_buy.set_case_id(bca.create_event("Check that child has Open status", self.test_id))
        self.fix_verifier_buy.check_fix_message_sequence([self.er_pending_new_dma_1_order_params, self.er_new_dma_1_order_params], key_parameters_list=[None, None], direction=self.ToQuod, pre_filter=None)
        # endregion
        
        # region Set up Open phase
        market_data_snap_shot_paris = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id_paris, self.fix_env1.feed_handler)
        market_data_snap_shot_paris.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.px_for_incr, MDEntrySize=self.qty_for_incr)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_paris)
        # endregion

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)
