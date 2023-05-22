import os
import sched
import time
from copy import deepcopy
from datetime import datetime, timedelta

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


class QAP_T11234(TestCase):
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
        self.qty = 1200
        self.indicative_volume = 1000
        self.percentage_volume = 10
        self.price = 30
        self.price2 = AFM.calc_ticks_offset_minus(self.price, 1, 0.005)

        self.price_ask = 40
        self.qty_ask = 1_000_000

        self.price_bid = 30
        self.qty_bid = 1_000_000

        self.pov_qty_child = AFM.get_pov_child_qty(self.percentage_volume, self.qty_bid, self.qty)

        self.tif_atc = TimeInForce.AtTheClose.value
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_cancel = Status.Cancel
        self.status_reached_uncross = Status.ReachedUncross
        self.status_eliminate = Status.Eliminate
        # endregion

        # region instrument
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.client = self.data_set.get_client_by_name("client_3")
        self.account = self.data_set.get_account_by_name("account_3")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        # endregion

        # region Key parameters       
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")
        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        self.rule_list = []

        self.pre_filter = self.data_set.get_pre_filter("pre_filer_equal_D")


    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        nos_rule = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.price)
        nos_rule2 = rule_manager.add_NewOrdSingleExecutionReportPendingAndNew(self.fix_env1.buy_side, self.account, self.mic, self.price2)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.mic)
        cancel_rule = rule_manager.add_OrderCancelRequest(self.fix_env1.buy_side, self.client, self.mic, True)
        self.rule_list = [nos_rule, nos_rule2, ocr_rule, ocrr_rule,  cancel_rule]
        # endregion

        # region EndDate for TradingPhases
        now = datetime.now()
        end_date_pre_close = now + timedelta(minutes=1)
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phases = AFM.get_timestamps_for_current_phase(TradingPhases.PreClosed)
        trading_phases = AFM.update_endtime_for_trading_phase_by_phase_name(trading_phases, TradingPhases.PreClosed, end_date_pre_close)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region

        # region Send MarketDate
        self.fix_manager_feed_handler.set_case_id(case_id=bca.create_event("Send trading phase - PreClose", self.test_id))
        self.incremental_refresh = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative() \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', 1000) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler) \
            .set_phase(TradingPhases.PreClosed)
        self.fix_manager_feed_handler.send_message(fix_message=self.incremental_refresh)
        # endregion

        # region Send NewOrderSingle
        case_id_1 = bca.create_event("Create TWAP Auction Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        # region Send POV algo
        self.pov_auction_algo = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_MOC_Auction_params()
        self.pov_auction_algo.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_auction_algo.change_parameters(dict(Account=self.client, OrderQty=self.qty, Price=self.price, Instrument=self.instrument, ExDestination=self.mic))
        self.pov_auction_algo.update_fields_in_component('QuodFlatParameters', dict(MaxParticipationClose=self.percentage_volume))
        self.fix_manager_sell.send_message_and_receive_response(fix_message=self.pov_auction_algo, case_id=case_id_1)
        # endregion

        # region Check Sell side
        self.fix_verifier_sell.check_fix_message(fix_message=self.pov_auction_algo, key_parameters=self.key_params_cl, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        er_pending_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_auction_algo, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(fix_message=er_pending_new, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        er_new = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_auction_algo, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(fix_message=er_new, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        scheduler = sched.scheduler(time.time, time.sleep)
        start_time_at_last = AFM.get_timestamp_from_list(phases=trading_phases, phase=TradingPhases.AtLast, start_time=True)
        self.verify_time = start_time_at_last + 5

        self.incremental_refresh_at_last = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_indicative() \
            .update_value_in_repeating_group('NoMDEntriesIR', 'MDEntrySize', self.indicative_volume) \
            .update_MDReqID(self.listing_id, self.fix_env1.feed_handler) \
            .set_phase(TradingPhases.AtLast)
        scheduler.enterabs(start_time_at_last, 1, self.fix_manager_feed_handler.set_case_id, kwargs=dict(case_id=bca.create_event("Send trading phase - AtLast", self.test_id)))
        scheduler.enterabs(start_time_at_last, 2, self.fix_manager_feed_handler.send_message, kwargs=dict(fix_message=self.incremental_refresh_at_last))

        # region Check auction child order
        case_id_2 = bca.create_event("Check auction child order", self.test_id)
        scheduler.enterabs(self.verify_time, 1, self.fix_verifier_buy.set_case_id, kwargs=dict(case_id=case_id_2))

        self.dma_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_DMA_RB_params()
        self.dma_order.change_parameters(dict(Account=self.account, ExDestination=self.mic, OrderQty=112, TimeInForce=self.tif_atc, Price=self.price, Instrument=self.instrument))
        scheduler.enterabs(self.verify_time, 2, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=self.dma_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle child order'))

        er_pending_new_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_pending)
        scheduler.enterabs(self.verify_time, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_pending_new_dma, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew child order'))

        er_new_dma = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.dma_order, self.gateway_side_buy, self.status_new)
        scheduler.enterabs(self.verify_time, 3, self.fix_verifier_buy.check_fix_message, kwargs=dict(fix_message=er_new_dma, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport child order'))
        # endregion
        scheduler.run()

        self.fix_verifier_sell.set_case_id(bca.create_event("Check that POV order is eliminated", self.test_id))
        er_cancel_auction_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_auction_algo, self.gateway_side_sell, self.status_reached_uncross)
        er_cancel_auction_order.add_tag(dict(Text='PARIS is closing'))
        self.fix_verifier_sell.check_fix_message(er_cancel_auction_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):

        time.sleep(2)
        rule_manager = RuleManager(Simulators.algo)
        rule_manager.remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phases = AFM.get_default_timestamp_for_trading_phase()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # end region
