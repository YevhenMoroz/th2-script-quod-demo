import os
import sched
import time

from pathlib import Path

import pytz

from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.algo_mongo_manager import AlgoMongoManager as AMM
from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, FreeNotesReject
from test_framework.db_wrapper.db_manager import DBManager
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager


class QAP_T9086(TestCase):
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
        self.qty = 1000
        self.indicative_volume_null = 0
        self.indicative_volume2 = 120
        self.historical_volume = 1200.0
        self.percentage = 10
        self.child_qty = AFM.get_child_qty_for_auction_historical_volume(self.historical_volume, self.percentage, self.qty)
        self.price = 80
        self.price2 = 79
        # endregion

        # region TimeInForce
        self.time_in_force_ATC = TimeInForce.AtTheClose.value
        self.time_in_force_ATO = TimeInForce.AtTheOpening.value
        # endregion

        # region FreeNotes
        self.reached_uncross = FreeNotesReject.ReachedUncross.value
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

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_21")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_19")
        self.mic = self.data_set.get_mic_by_name("mic_31")
        # endregion

        # region Key parameters
        self.key_params_ER_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params_with_ex_destination = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_child")
        self.key_params_NOS_parent = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_NOS_parent")
        self.key_params_ER_child = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_ER_child")
        # endregion

        self.listing_id = self.data_set.get_listing_id_by_name("listing_37")
        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile2")
        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.price)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.mic)
        self.rule_list = [nos_rule, ocr_rule, ocrr_rule]
        # endregion


        # region Update Trading Phase

        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region insert data into mongoDB

        curve = AMM.get_straight_curve_for_mongo(trading_phases, volume=self.historical_volume)
        self.db_manager.insert_many_to_mongodb_with_drop(curve, f"Q{self.listing_id}")
        bca.create_event("Data in mongo inserted", self.test_id)
        # endregion

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase PreClosed", self.test_id))
        self.incremental_refresh_pre_close = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative().update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume_null).update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase("4")
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh_pre_close)
        # endregion

        # region Send NewOrderSingle
        case_id_1 = bca.create_event("Create Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_MOC_params()
        self.auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.auction_algo.update_fields_in_component("QuodFlatParameters", dict(MaxParticipation=self.percentage))
        responce = self.fix_manager_sell.send_message_and_receive_response(self.auction_algo, case_id_1)[0]

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(self.auction_algo, key_parameters=self.key_params_NOS_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_pending)
        er_pending_new.change_parameters(dict(TimeInForce=self.time_in_force_ATC))
        self.fix_verifier_sell.check_fix_message(er_pending_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport PendingNew')

        er_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_new)
        er_new.change_parameters(dict(TimeInForce=self.time_in_force_ATC))
        self.fix_verifier_sell.check_fix_message(er_new, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport New')
        # endregion


        scheduler = sched.scheduler(time.time, time.sleep)

        end_time_preclosed = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.PreClosed, start_time=False)
        self.verifier_time = end_time_preclosed + 5

        auction_cancel_time_start = AFM.change_datetime_from_epoch_to_normal(end_time_preclosed -30).astimezone(pytz.utc).isoformat()[:-6]
        auction_cancel_time_end = AFM.change_datetime_from_epoch_to_normal(end_time_preclosed-15).astimezone(pytz.utc).isoformat()[:-6]

        # region check child order
        scheduler.enterabs(self.verifier_time, 1, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=bca.create_event("Check child order", self.test_id)))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=self.child_qty, Price=self.price, TimeInForce=self.time_in_force_ATC, Instrument=self.instrument))
        scheduler.enterabs(self.verifier_time, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.dma_order, key_parameters=self.key_params_with_ex_destination, message_name='Buy side NewOrderSingle child order'))

        er_pending_new_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(self.verifier_time, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_pending_new_dma, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew child order'))

        er_new_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(self.verifier_time, 4, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_new_dma, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport New child order'))

        er_new_canceled = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
        er_new_canceled.change_parameter("TransactTime", ">" + auction_cancel_time_start)
        scheduler.enterabs(self.verifier_time, 5, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_new_canceled, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Canceled child order'))

        er_new_canceled2 = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_cancel)
        er_new_canceled2.change_parameter("TransactTime", "<" + auction_cancel_time_end)
        scheduler.enterabs(self.verifier_time, 5, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_new_canceled2, key_parameters=self.key_params_ER_child, direction=self.ToQuod, message_name='Buy side ExecReport Canceled child order'))

        # endregion

        auction_child_time = AFM.change_datetime_from_epoch_to_normal(end_time_preclosed).astimezone(pytz.utc).isoformat()[:-6]
        self.dma_order.change_parameter("TransactTime", ">" + auction_child_time)

        scheduler.enterabs(end_time_preclosed- 32, 1, self.fix_manager_feed_handler.set_case_id,kwargs=dict(case_id=bca.create_event("Send trading phase PreClosed with volume before 30 sec checkpoint", self.test_id)))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative()\
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume2)\
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.price2)\
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase("4")
        scheduler.enterabs(end_time_preclosed - 32, 1, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh))


        scheduler.enterabs(end_time_preclosed- 29, 1, self.fix_manager_feed_handler.set_case_id,kwargs=dict(case_id=bca.create_event("Send trading phase PreClosed without volume after 30 sec checkpoint", self.test_id)))
        scheduler.enterabs(end_time_preclosed - 29, 2, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_pre_close))

        self.incremental_refresh_atlast = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative()\
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume_null) \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntryPx', self.price2) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase("5")
        scheduler.enterabs(end_time_preclosed + 1, 1, self.fix_manager_feed_handler.set_case_id,kwargs=dict(case_id=bca.create_event("Send trading phase AtLast", self.test_id)))
        scheduler.enterabs(end_time_preclosed + 1, 2, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_atlast))


        scheduler.run()

        time.sleep(3)
        # region Cancel Algo Order
        case_id_2 = bca.create_event("Check that algo order is canceled", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_2)

        er_cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.auction_algo, self.gateway_side_sell, self.status_cancel)
        er_cancel_auction_order.add_tag(dict(SettlDate='*')).change_parameters(dict(TimeInForce=self.time_in_force_ATC, Text=self.reached_uncross, LastMkt=self.mic)).remove_parameter('OrigClOrdID')
        self.fix_verifier_sell.check_fix_message(er_cancel_auction_order, key_parameters=self.key_params_ER_parent, message_name='Sell side ExecReport Cancel')
        # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        self.db_manager.drop_collection(f"Q{self.listing_id}")
        bca.create_event(f"Collection QP{self.listing_id} is dropped", self.test_id)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region
