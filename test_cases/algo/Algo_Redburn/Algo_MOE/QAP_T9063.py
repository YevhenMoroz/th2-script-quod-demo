import os
import sched
import time

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, RBCustomTags
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.db_wrapper.db_manager import DBManager


class QAP_T9063(TestCase):
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
        # endregion

        # region order parameters
        self.tif_gtc = TimeInForce.GoodTillCrossing.value
        self.tif_gft = TimeInForce.GoodForTime.value

        self.rb_custom_tag = RBCustomTags.RedburnCustomFields.value


        self.qty = 1_000_000
        self.indicative_volume = 1_000
        self.indicative_price = 100
        self.percentage = 10
        self.child_qty = self.qty
        self.price = 130
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_partial_fill = Status.PartialFill
        self.status_rejected = Status.Reject
        self.status_cancel = Status.Cancel
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.ex_destination_1 = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name("account_2")
        self.s_par = self.data_set.get_listing_id_by_name("listing_36")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price)
        nos_trade_rule = rule_manager.add_NewOrdSingleExecutionReportTradeByOrdQtyRBCustom(self.fix_env1.buy_side, self.account, self.ex_destination_1, self.price, self.price, 112, 50, 0)
        cancel_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        self.rule_list = [nos_rule, nos_trade_rule, cancel_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.Expiry)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Mongo insert
        self.db_manager.create_empty_collection(collection_name=f"Q{self.s_par}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Expiry", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_MDReqID(self.s_par, self.fix_env1.feed_handler).set_phase(TradingPhases.Expiry)
        self.incremental_refresh.update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.indicative_price)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle (35=D) for MP Dark order
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOE_params()
        self.auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument))
        self.auction_algo.update_fields_in_component("QuodFlatParameters", dict(MaxParticipation=self.percentage))
        self.fix_manager_sell.send_message_and_receive_response(self.auction_algo, case_id_1)

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.auction_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_pending)
        pending_auction_order_params.change_parameters(dict(TimeInForce=self.tif_gtc))
        self.fix_verifier_sell.check_fix_message(pending_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_auction_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_new)
        new_auction_order_params.change_parameters(dict(TimeInForce=self.tif_gtc))
        self.fix_verifier_sell.check_fix_message(new_auction_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        # region check child order
        case_id_2 = bca.create_event("Check child order", self.test_id)
        self.fix_verifier_buy.set_case_id(case_id_2)

        scheduler = sched.scheduler(time.time, time.sleep)
        end_time = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Expiry, start_time=False) / 1000
        start_time = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.Expiry, start_time=True) / 1000
        release_time = AFM.change_datetime_from_epoch_to_normal(start_time).astimezone(pytz.utc).isoformat()[:-6]

        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - Open", self.test_id))

        self.open_phase = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume).update_MDReqID(self.s_par, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        scheduler.enterabs(start_time + 20, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.open_phase))

        dma_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        dma_order.change_parameters(dict(OrderQty=112, Price=self.price, Instrument='*', TimeInForce=self.tif_gft))
        scheduler.enterabs(start_time + 10, 1, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle Child'))

        pending_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(start_time + 10, 1, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=pending_dma_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew Child'))

        new_dma_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(start_time + 10, 1, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=new_dma_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New Child'))

        partial_fill_dma_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(dma_order, self.gateway_side_buy, self.status_partial_fill)
        partial_fill_dma_child_order.change_parameters(dict(TimeInForce=self.tif_gft))
        partial_fill_dma_child_order.add_tag(dict(RedburnCustomFields = self.rb_custom_tag))
        scheduler.enterabs(start_time + 15, 1, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=partial_fill_dma_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy Side ExecReport Partial Fill Child'))
        # endregion

        partial_fill_auction_algo_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_partial_fill)
        partial_fill_auction_algo_order.change_parameters(dict(TimeInForce=self.tif_gtc))
        partial_fill_auction_algo_order.add_tag(dict(RedburnCustomFields = self.rb_custom_tag))
        scheduler.enterabs(start_time + 20, 1, self.fix_verifier_sell.check_fix_message, kwargs=dict(fix_message=partial_fill_auction_algo_order, key_parameters=self.key_params, message_name='Sell Side ExecReport Partial Fill Auction'))

        scheduler.run()

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_3 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_3)
        # endregion

        cancel_request_auction_order = FixMessageOrderCancelRequest(self.auction_algo)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_auction_order, case_id_3)
        self.fix_verifier_sell.check_fix_message(cancel_request_auction_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(5)

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.s_par}")
        bca.create_event(f"Collection QP{self.s_par} is dropped", self.test_id)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region check cancellation parent Auction order
        cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_cancel)
        cancel_auction_order.change_parameters(dict(TimeInForce=self.tif_gtc))
        self.fix_verifier_sell.check_fix_message(cancel_auction_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion