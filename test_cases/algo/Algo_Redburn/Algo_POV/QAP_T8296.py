import os
import time
from datetime import datetime, timedelta
from pathlib import Path

from test_framework.core.try_exept_decorator import try_except
from custom import basic_custom_actions as bca
from rule_management import RuleManager, Simulators
from test_framework.data_sets.constants import DirectionEnum, Status, GatewaySide, TradingPhases, TimeInForce, OrderType
from test_framework.fix_wrappers.algo.FixMessageNewOrderSingleAlgo import FixMessageNewOrderSingleAlgo
from test_framework.fix_wrappers.algo.FixMessageExecutionReportAlgo import FixMessageExecutionReportAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataSnapshotFullRefreshAlgo import FixMessageMarketDataSnapshotFullRefreshAlgo
from test_framework.fix_wrappers.algo.FixMessageMarketDataIncrementalRefreshAlgo import FixMessageMarketDataIncrementalRefreshAlgo
from test_framework.fix_wrappers.FixManager import FixManager
from test_framework.fix_wrappers.FixVerifier import FixVerifier
from test_framework.core.test_case import TestCase
from test_framework.data_sets import constants
from test_framework.fix_wrappers.FixMessageOrderCancelRequest import FixMessageOrderCancelRequest
from test_framework.algo_formulas_manager import AlgoFormulasManager as AFM
from test_framework.rest_api_wrappers.algo.RestApiStrategyManager import RestApiAlgoManager
from test_framework.ssh_wrappers.ssh_client import SshClient
from test_framework.formulas_and_calculation.trading_phase_manager import TradingPhaseManager, TimeSlot

class QAP_T8296(TestCase):
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
        # endregion

        # region order parameters
        self.order_type = constants.OrderType.Market.value
        self.tif_day = constants.TimeInForce.Day.value
        self.tif_ioc = constants.TimeInForce.ImmediateOrCancel.value

        self.percentage_volume = 40
        self.min_participation = 20
        
        self.qty = 500000
        # self.price = 35

        self.price_ltq_0 = 0
        self.qty_ltq_0 = 0

        self.price_ltq_1 = 40
        self.qty_ltq_1 = 20_000

        self.price_ask_1 = 40
        self.qty_ask_1 = 50_000

        self.price_bid_1 = 0
        self.qty_bid_1 = 0

        self.reactive_child_qty = AFM.get_pov_child_qty_on_ltq(self.percentage_volume, self.qty_ltq_1, self.qty)
        # endregion

        # region Gateway Side
        self.gateway_side_buy = GatewaySide.RBBuy
        self.gateway_side_sell = GatewaySide.RBSell
        # endregion

        # region Status
        self.status_pending = Status.Pending
        self.status_new = Status.New
        self.status_eliminated = Status.Eliminate
        self.status_cancel = Status.Cancel
        # endregion

        # region Direction
        self.FromQuod = DirectionEnum.FromQuod
        self.ToQuod = DirectionEnum.ToQuod
        # endregion

        # region venue param
        self.instrument = self.data_set.get_fix_instrument_by_name("instrument_1")
        self.mic = self.data_set.get_mic_by_name("mic_1")
        self.client = self.data_set.get_client_by_name("client_2")
        self.account = self.data_set.get_account_by_name('account_2')
        self.listing_id = self.data_set.get_listing_id_by_name("listing_36")

        self.trading_phase_profile = self.data_set.get_trading_phase_profile("trading_phase_profile1")
        # endregion

        # region Key parameters
        self.key_params_cl = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_1")
        self.key_params = self.data_set.get_verifier_key_parameters_by_name("verifier_key_parameters_2")
        # endregion

        self.rule_list = []

        self.rest_api_manager = RestApiAlgoManager(session_alias=self.restapi_env1.session_alias_wa, case_id=self.test_id)

    @try_except(test_id=Path(__file__).name[:-3])
    def run_pre_conditions_and_steps(self):
        # region Rule creation
        rule_manager = RuleManager(Simulators.algo)
        # nos_ioc_rule_1 = rule_manager.add_NewOrdSingleExecutionReportIOCAll(self.fix_env1.buy_side, self.account, self.mic)
        not_ioc_trade_rule = rule_manager.add_NewOrdSingle_IOCTradeOnFullQty(self.fix_env1.buy_side, self.account, self.mic, True, self.price_ask_1)
        ocr_rule = rule_manager.add_OCR(self.fix_env1.buy_side)
        ocrr_rule = rule_manager.add_OrderCancelReplaceRequest(self.fix_env1.buy_side, self.account, self.mic)
        self.rule_list = [not_ioc_trade_rule, ocr_rule, ocrr_rule]
        # endregion

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Modify trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_timestamps_for_trading_phase_sequence(TradingPhases.Open)
        trading_phases = trading_phase_manager.get_trading_phase_list()
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region Clear Market Data
        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq_0, MDEntrySize=self.price_ltq_0)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_bid_1, MDEntrySize=self.qty_bid_1)
        market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask_1, MDEntrySize=self.qty_ask_1)
        self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)

        self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq_1, MDEntrySize=self.qty_ltq_1)
        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(3)
        # endregion

        # region Send NewOrderSingle (35=D) for POV order
        case_id_1 = bca.create_event("Create POV Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_1)

        self.pov_order = FixMessageNewOrderSingleAlgo(data_set=self.data_set).set_POV_Redburn_params()
        self.pov_order.add_ClordId((os.path.basename(__file__)[:-3]))
        self.pov_order.change_parameters(dict(Account=self.client, OrderQty=self.qty, OrdType=self.order_type, Instrument=self.instrument, ExDestination=self.mic))
        self.pov_order.remove_parameter('Price')
        self.pov_order.update_fields_in_component('QuodFlatParameters', dict(MaxPercentageVolume=self.percentage_volume, MinParticipation=self.min_participation))
        self.fix_manager_sell.send_message_and_receive_response(self.pov_order, case_id_1)

        time.sleep(3)
        # endregion

        # region Check Sell side
        nos_pov_parent = self.pov_order.change_parameter('TransactTime', '*')
        self.fix_verifier_sell.check_fix_message(nos_pov_parent, direction=self.ToQuod, message_name='Sell side NewOrderSingle')

        pending_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_pending)
        self.fix_verifier_sell.check_fix_message(pending_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport PendingNew')

        new_pov_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_new)
        self.fix_verifier_sell.check_fix_message(new_pov_order_params, key_parameters=self.key_params_cl, message_name='Sell side ExecReport New')
        # endregion

        self.fix_manager_feed_handler.send_message(market_data_incremental_par)

        time.sleep(5)
        # # region Check DMA child order 1
        # self.case_id_2 = bca.create_event("DMA child order - level 1", self.test_id)
        # self.fix_verifier_buy.set_case_id(self.case_id_2)
        #
        # anticipative_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        # anticipative_child_order.change_parameters(dict(Account=self.account, OrderQty=self.anticipative_child_qty, Price=self.price_bid_1, Instrument='*', ExDestination=self.mic))
        # self.fix_verifier_buy.check_fix_message(anticipative_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 1')
        #
        # pending_anticipative_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(anticipative_child_order, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(pending_anticipative_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 1')
        #
        # new_anticipative_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(anticipative_child_order, self.gateway_side_buy, self.status_new)
        # self.fix_verifier_buy.check_fix_message(new_anticipative_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New  DMA Child 1')
        #
        # # region Send new Incremental refresh to trigger the Reactive child order generation
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data Incremental to clear the MarketDepth", self.test_id))
        # market_data_incremental_par = FixMessageMarketDataIncrementalRefreshAlgo().set_market_data_incr_refresh_ltq().update_MDReqID(self.listing_id, self.fix_env1.feed_handler).set_phase(TradingPhases.Open)
        # market_data_incremental_par.update_repeating_group_by_index('NoMDEntriesIR', 0, MDEntryPx=self.price_ltq_1, MDEntrySize=self.qty_ltq_1)
        # self.fix_manager_feed_handler.send_message(market_data_incremental_par)
        #
        # time.sleep(1)
        #
        # self.fix_manager_feed_handler.set_case_id(bca.create_event("Send Market Data SnapShot to clear the MarketDepth", self.test_id))
        # market_data_snap_shot_par = FixMessageMarketDataSnapshotFullRefreshAlgo().set_market_data().update_MDReqID(self.listing_id, self.fix_env1.feed_handler)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 0, MDEntryPx=self.price_ltq_0, MDEntrySize=self.price_ltq_0)
        # market_data_snap_shot_par.update_repeating_group_by_index('NoMDEntries', 1, MDEntryPx=self.price_ask, MDEntrySize=self.qty_ask)
        # self.fix_manager_feed_handler.send_message(market_data_snap_shot_par)
        # # endregion
        #
        # time.sleep(4)
        #
        # cancel_dma_child_1_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(anticipative_child_order, self.gateway_side_buy, self.status_cancel)
        # self.fix_verifier_buy.check_fix_message(cancel_dma_child_1_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel DMA 1 child')
        # # endregion
        #
        # # region Check DMA child order 2
        # self.case_id_3 = bca.create_event("IOC DMA child order - level 2", self.test_id)
        # self.fix_verifier_buy.set_case_id(self.case_id_3)
        #
        # self.reactive_child_order = FixMessageNewOrderSingleAlgo().set_DMA_RB_params()
        # self.reactive_child_order.change_parameters(dict(Account=self.account, OrderQty=self.reactive_child_qty, Price=self.price, Instrument='*', ExDestination=self.mic, TimeInForce=self.tif_ioc))
        # self.fix_verifier_buy.check_fix_message(self.reactive_child_order, key_parameters=self.key_params, message_name='Buy side NewOrderSingle DMA Child 2')
        #
        # pending_reactive_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.reactive_child_order, self.gateway_side_buy, self.status_pending)
        # self.fix_verifier_buy.check_fix_message(pending_reactive_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport PendingNew DMA Child 2')
        #
        # new_reactive_child_order_params = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.reactive_child_order, self.gateway_side_buy, self.status_new)
        # self.fix_verifier_buy.check_fix_message(new_reactive_child_order_params, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport New DMA Child 2')
        #
        # # region Cancel POV DMA child order
        # eliminate_reactive_child_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.reactive_child_order, self.gateway_side_buy, self.status_eliminated)
        # self.fix_verifier_buy.check_fix_message(eliminate_reactive_child_order, key_parameters=self.key_params, direction=self.ToQuod, message_name='Buy side ExecReport Cancel DMA 2 child')
        # # endregion
        # # endregion

    @try_except(test_id=Path(__file__).name[:-3])
    def run_post_conditions(self):
        # region Check eliminated Algo Order
        case_id_5 = bca.create_event("Cancel parent Algo Order", self.test_id)
        self.fix_verifier_sell.set_case_id(case_id_5)
        # endregion

        cancel_request_pov_order = FixMessageOrderCancelRequest(self.pov_order)
        self.fix_manager_sell.send_message_and_receive_response(cancel_request_pov_order, case_id_5)
        self.fix_verifier_sell.check_fix_message(cancel_request_pov_order, direction=self.ToQuod, message_name='Sell side Cancel Request')

        time.sleep(3)

        RuleManager(Simulators.algo).remove_rules(self.rule_list)

        # region Update Trading Phase
        self.rest_api_manager.set_case_id(case_id=bca.create_event("Revert trading phase profile", self.test_id))
        trading_phase_manager = TradingPhaseManager()
        trading_phase_manager.build_default_timestamp_for_trading_phase()
        trading_phases = trading_phase_manager.get_trading_phase_list(new_standard=False)
        self.rest_api_manager.modify_trading_phase_profile(self.trading_phase_profile, trading_phases)
        # endregion

        # region check cancellation parent POV order
        cancel_pov_order = FixMessageExecutionReportAlgo().set_params_from_new_order_single(self.pov_order, self.gateway_side_sell, self.status_cancel)
        self.fix_verifier_sell.check_fix_message(cancel_pov_order, key_parameters=self.key_params_cl, message_name='Sell side ExecReport Cancel')
        # endregion