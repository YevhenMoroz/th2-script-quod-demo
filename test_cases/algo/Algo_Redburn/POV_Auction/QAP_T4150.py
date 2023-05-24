import os
import sched
import time
from copy import deepcopy

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from datetime import datetime, timedelta, timezone
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot


class QAP_T4150(TestCase):
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
        self.restapi_env1 = self.environment.get_list_web_admin_rest_api_environment()[0]
        self.db_manager = DBManager(self.environment.get_list_data_base_environment()[0])
        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)
        # endregion

        # region order parameters
        self.qty = 1_000_000
        self.indicative_volume = 0
        self.percentage_volume = 10
        self.price = 130
        self.price2 = 30
        
        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 100_000
        self.qty_bid_2 = 200_000

        self.last_trade_qty = 0
        self.last_trade_price = 0

        self.navigator_limit_price = 25

        self.pov_qty_child = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)
        self.pov_qty_child_2 = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid_2, self.qty)
        self.navigator_child_qty = self.qty - AFM.get_nav_reserve(self.qty, self.pov_qty_child)

        self.tif_atc = TimeInForce.AtTheClose.value

        self.check_order_sequence = False

        self.pre_filter_cancel = self.data_set.get_pre_filter('pre_filer_equal_ER_canceled')
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        # self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # self.client = self.data_set.get_client_by_name("client_2")
        # self.account = self.data_set.get_account_by_name("account_2")
        # self.mic = self.data_set.get_mic_by_name("mic_1")
        # self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        #
        # self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")

        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_21")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_18")
        self.mic = self.data_set.get_mic_by_name("mic_31")
        self.listing_id = self.data_set.get_listing_id_by_name("listing_37")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile2")
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
        nos_rule = rule_manager.add_NewOrdSingle_IOC(self.fix_env1.buy_side, self.account, self.mic, False, 0, self.price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.price2)
        nos_rule3 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.navigator_limit_price)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.mic)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.mic, True)
        self.rule_list = [nos_rule, nos_rule2, nos_rule3, ocr_rule, ocrr_rule,  cancel_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid, MDEntryPositionNo=1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.last_trade_price, MDEntrySize=self.last_trade_qty)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        # region Send NewOrderSingle (35=D)
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Send TWAP algo
        self.pov_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Navigator_params()
        self.pov_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.pov_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipation=self.percentage_volume, NavigatorLimitPrice=self.navigator_limit_price))
        self.fix_manager_sell.send_message_and_receive_response(fix_message=self.pov_algo, case_id=case_id_1)
        # endregion

        # region Check Sell side
        self.auction_algo_verification = deepcopy(self.pov_algo)
        self.fix_verifier_sell.check_fix_message(fix_message=self.auction_algo_verification, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(fix_message=er_pending_new, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        er_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(fix_message=er_new, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        self.incremental_refresh_pre_auction = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative() \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler) \
            .set_phase(TradingPhases.Auction)

        time.sleep(3)
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Auction", self.test_id))
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh_pre_auction)

        # region Check that POV cancel benchmark child
        time.sleep(3)
        case_id_2 = bca.create_event("Check that POV benchmark child 1", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        passive_child_order_1 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        passive_child_order_1.change_parameters(dict(Account=self.account, OrderQty=self.pov_qty_child, Price=self.price_bid, Instrument='*', ExDestination=self.mic))
        self.fix_verifier_buy.check_fix_message(passive_child_order_1, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 1')

        pending_passive_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(fix_message=pending_passive_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 1')

        new_passive_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(fix_message=new_passive_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 1')

        cancel_pov_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(passive_child_order_1, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message_sequence([cancel_pov_dma_child_order], [self.key_params], direction=self.ToQuod, pre_filter=self.pre_filter_cancel, message_name='Buy side ExecReport Canceled Auction child order', check_order=self.check_order_sequence)
        # endregion

        # region Check Navigator child order
        self.case_id_3 = bca.create_event("Check that POV Navigator child 1", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_3)

        self.navigator_child = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.navigator_child.change_parameters(dict(Account=self.account, OrderQty=self.navigator_child_qty, Price=self.navigator_limit_price, Instrument='*', ExDestination=self.mic))
        self.fix_verifier_buy.check_fix_message(self.navigator_child, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Navigator Child 1')

        pending_navigator_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(fix_message=pending_navigator_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Navigator Child 1')

        new_navigator_child_order_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(fix_message=new_navigator_child_order_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Navigator Child 1')
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to change AUC phase into OPN", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid, MDEntrySize=self.qty_bid_2, MDEntryPositionNo=1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.last_trade_price, MDEntrySize=self.last_trade_qty)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        # endregion

        time.sleep(2)

        self.case_id_4 = bca.create_event("Check that POV benchmark child 2", self.test_id)
        self.fix_verifier_buy.set_case_id(self.case_id_4)

        self.passive_child_order_2 = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        self.passive_child_order_2.change_parameters(dict(Account=self.account, OrderQty=self.pov_qty_child_2, Price=self.price_bid, Instrument='*', ExDestination=self.mic))
        self.fix_verifier_buy.check_fix_message(self.passive_child_order_2, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 2')

        pending_passive_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_2, self.gateway_side_buy, self.status_pending)
        self.fix_verifier_buy.check_fix_message(fix_message=pending_passive_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 2')

        new_passive_child_order_2_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_2, self.gateway_side_buy, self.status_new)
        self.fix_verifier_buy.check_fix_message(fix_message=new_passive_child_order_2_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 2')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(3)
        # region Cancel Algo Order
        case_id_5 = bca.create_event("Cancel Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_5)
        cancel_request_auction_order = FixMessageOrderCancelRequest(self.pov_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_5)
        # endregion

        time.sleep(2)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        self.fix_verifier_buy.set_case_id(self.case_id_3)
        cancel_pov_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.navigator_child, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_pov_dma_child_order, self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Canceled Navigator child order')

        self.fix_verifier_buy.set_case_id(self.case_id_4)
        cancel_pov_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.passive_child_order_2, self.gateway_side_buy, self.status_cancel)
        self.fix_verifier_buy.check_fix_message(cancel_pov_dma_child_order, self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Canceled POV child order')

        er_cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_algo, self.gateway_side_sell, self.status_cancel)
        er_cancel_auction_order.add_tag(dict(OrigClOrdID='*'))
        self.fix_verifier_sell.check_fix_message(er_cancel_auction_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')